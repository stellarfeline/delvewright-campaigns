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

## Step 8b — the showcase cameras

Sixteen cameras, one per approved picture, estimated from the pictures and moved on the built tree with `delvec cameras --draft` until each frames its subject (`design/cameras.json`, all `estimated`). The four inside the maze's courts and the gate hall were moved once: the first estimates stood in a wall or faced one.

## Step 11 — the branch chronicle

One fork, `branch-point/who-comes-out`, three story worlds (`world/0` and `world/2` reach `ending/together`, `world/1` reaches `ending/alone`). Read end to end. One finding on the first read: the finale's own `happening` said *the friends walk out to the gardener* on every world, the alone world included; it now says the way out is open, and the endings say who walks out. Line numbers below are the re-read chronicles.

| claim reviewed (dialogue/design beat) | branch | chronicle line(s) | verdict |
|---|---|---|---|
| Wren: "you're out, both of you … you came over the bridge?" (`dlg/wren-together`) | `branch/together` (`world/0`, `world/2`) | flag assignment `flag/crossed-the-bridge=set`; 16/13 the bridge rises; 19/16 `departs` together | cleared |
| Wren: "I was frightened just watching you come over it." | `branch/together` | as above | cleared |
| Wren: "Is there anyone else in there? … the bridge is up now" (`dlg/wren-alone`) | `branch/alone` (`world/1`) | flag `unset`; 13 the bridge rises; 16 `departs` alone | cleared |
| Option "Just me tonight." ends the delve alone | `branch/alone` | 16 `departs` alone | cleared |
| Option "I'll wait for them." closes the talk, no ending | `branch/alone` | no line (no effect) | cleared |
| The Listener "sleeps under the old well … Tonight it didn't." (both trees) | both | 8 the sleeper digs up by the well | cleared |
| DESIGN §5: the sleeper is never beaten in either ending | both | no `dies` line on any world | cleared |
| Finale `happening` "the friends walk out" on the alone world | `branch/alone` | 9 (first read) | **FINDING**, fixed: the happening now says the way out is open |

### Step 9, after the cross and the visual review

The lookout became a cross of four arms 24 blocks long (a ruling of the person's, given when the deck alone showed the runner in 38 % of lane cells); the bridge was shortened to run on from the east arm. Wave bound: `concurrency: 5 = min(7, max(1, 10 / 2))`.

| place | attempt | tokens | duration | repaired | commit exit |
|---|---|---|---|---|---|
| node/bridge | 2 | 76957 | 75 s | `DW0843` (the old frame) | 3 (battery: the maze stand-in) |
| node/arm-north | 1 | 110850 | 154 s | — | 3 (battery) |
| node/lookout | 3 | 92842 | 194 s | `DW0844` (the four arm seams) | 3 (battery) |
| node/arm-south | 1 | 108800 | 155 s | — | 3 (battery) |
| node/arm-west | 1 | 105077 | 172 s | — | 3 (battery) |
| node/arm-east | 1 | 187198 | 625 s | — | 3 (battery) |
| node/maze | 2 | 163227 | 654 s | `DW0322` (a way onto the wall tops) | 3 (battery: `DW0921`, the lawn) |
| node/meadow | 2 | 111094 | 137 s | `DW0921` (the meadow opens onto the lawn) | 3 (battery: `DW0881`, `DW0429`) |
| node/arm-east | 2 | 96545 | 111 s | `DW0429` (the chain post beside the bar) | 3 (battery: `DW0429` at the far end) |
| node/gate-top | 3 | 98078 | 145 s | `DW0429` | not committed: no cell can answer the bridge's far bar (`DW0429` against `DW0845`); the hatch was shut instead |
| node/bridge | 3 | 82369 | 61 s | `DW0844` (no bar at the far end) | 0 |
| node/gate-top | 4 | 81190 | 79 s | `DW0845` (the hatch's bar) | 0 |
| node/maze | 3 | 106518 | 131 s | visual review: the quarters' floors | 0 |

From the arms' rails, measured by sight lines over the built pieces (`.scratch` measurement, 104 eye points along the deck rail and the arms' rails, 4,837 lane cells, leaves opaque): a standing runner's head is seen in 67 % of lane cells (14 % within 15 blocks of the tower, under the arms' own decks; 78 % at 15–30; 72 % at 30–45; 66 % beyond 45), the warden's head in 80 %. From the deck's rail alone, before the arms: 3 % and 11 %.

## Step 10 — the machine ladder

On the build with manifest `ccc71c49aa708b5547401e2d828b331f9a3f9ec86dec451a2032166cb74186ab`, run on the remote build machine from the engine tree at `ffe9b58ae`:

- **Bot, critical path**: passed, 8 steps. **`pursuit` bound**: 3 pursued steps of 8 (reach the gate tower, wind the gate, meet Wren), 1 pursuer (`actor/the-sleeper`), 55 readings, closest approach 27.73 blocks; the bot walked out alive. `[sculk]` darkness 0, warden spawns heard 1. `[watch]` 1 watcher asserted. Die-retry unbound: no mandatory encounter.
- **Branch runs**: `world/0`, `world/1`, `world/2` ran and passed.
- **PackTest**: red, 1 required test: the generated `wave_census_yellow_slimes` sets one body's health to 1.0 and expects it counted damaged, and a small slime's maximum health is 1. An engine defect, reported; the campaign is unchanged.
- **Written world**: `DW0955` on 4 cells: the engine's load world holds a redstone block at each bell's power cell, which only a press of that bell's button sets for four ticks; the server holds air. An engine defect in the model, reported.
- **Staging gate**: refused on one ledger row, `doune-04` UNBOUND (the equipment check over an actor that wears nothing).

## Step 12 — visual review

`renderer: lumenwright 0.3.0, backend apple m2 pro (metal)`. 158 POV frames read in route order (sampled every fourth frame and every leg end on contact sheets), 19 threshold frames read blind, 3 cutscene frames, 16 showcase cameras.

- The lanes read as the approved lane picture: walls above the eye, hedge caps, the tower over the wall tops.
- Finding, fixed: the quarters' floors in terracotta read lavender, ochre and olive against the approved sky blue, butter yellow and mint; the maze was re-detailed in concrete powder (attempt 3).
- Threshold read: 19 frames — the deck with its counters and coloured panels, the arms and the bridge, the gate hall with the winch and the portcullis, the gate tower's roof, the meadow. Trade misses 0, front misses 0.
- The heart court is tighter than the approved heart picture: the tower fills most of it. Not changed.
- The gate hall's interior renders dark in the showcase camera.

## Findings ledger

| # | finding (as reported) | round | status |
|---|---|---|---|
| 1 | The warden rises too far from where the runner takes the crank; roaming, it only paces round its well and is barely felt. | 1 | fixed@r2 |
| 2 | Pressing a bell button lures the warden, but the players hear nothing. | 2 | fixed@r3 |
| 3 | The lookout's arms and deck hide the lanes below them. | 2 | fixed@r3 |

## Round 2 — the sleeper wakes near the sundial

- Finding 1 is content, not a capability gap. The ruling: the warden's emergence stands within its hearing of the crank, so a runner who runs off instead of sneaking is heard at once (it turns toward the sound, not yet hunting); the seven deaf seconds of the emerge are the runner's grace. No anger is seeded: the warden drifts toward a stationary player from 20–24 blocks on its own (the T11 controls).
- The old well moved into the rose quarter: its mouth is 12.1 blocks from the crank's frame, two turns and 20 blocks of lane away, out of sight of the sundial court (5,625 sight lines tested by the generator, none open). The sundial court has four ways out; a loop of 72.8 blocks back through the heart passes beyond 16 blocks of the well after 7.7 blocks; no dead end lies within 16 blocks of the well (nearest 16.3); the ways to the heart and the gate never come nearer the well than the sundial. Maze attempt 4; the note's line about the well, `DESIGN.md` and the two well cameras follow it.
- Machine record: one validation loop to green at build; DW codes hit: none new (the build's standing warnings `DW0822`, `DW0813`, `DW0781`, `DW1076`, `DW0451` x1).
- General form, for the engine's cross-campaign ledger (not written here, the engine tree is read-only to this round): a body declared `outrun` whose entrance stands beyond its kind's hearing reach of the beat that unleashes it is a pursuit nobody feels — a candidate advisory measuring the unleash point to the entrance against the kind's hearing.
- Ladder on the round-2 build (manifest `e5dee100017b6a431d8c60d34c40c492d87306824e293b4eadd66537c9a116aa`): bot critical path passed, 8 steps; `[pursuit] 3 pursued step(s) of 8, 1 pursuer(s), 34 reading(s); closest approach 12.98 block(s)` (27.73 in round 1). Branch runs: `world/0`, `world/1`, `world/2` ran and passed (closest approaches 2.04, 15.27 and 9.48 blocks; no death). PackTest: the same one red (`wave_census_yellow_slimes`, the engine's census test on a body of maximum health 1). Written world: the same `DW0955` on the four bell power cells. Staging gate: the same `doune-04` UNBOUND.

## Round 3 — the bells are heard, the cross is glass

- Finding 2: each bell button now also plays `minecraft:block.bell.use` at the bell for every player, volume 4 (heard to 64 blocks: the far arm tips to the far bells are about 57), category `block`, beside the redstone pulse. The pulse is what the warden hears (`warden-behaviour.md` §5: a played sound is not a vibration), and it is unchanged. Emitted as `playsound minecraft:block.bell.use block @a <bell> 4` in each `trig_ring_<colour>_bell`.
- Finding 3: the lookout's deck (inside a spruce rim) and the four arms are floored in clear glass, on dark oak beams under the rails only. Rails unchanged and unjumpable; the build's leak, soft-lock and boundary proofs (`DW0838`, `DW0921`, `DW0322`) are clean.
- Sight lines over the built pieces (glass counted see-through, leaves opaque; 104 eye points at the deck rail and the arm rails; 4,875 lane cells): a standing runner's head is seen in 86 % of lane cells (98 % within 15 blocks, 98 % at 15–30, 80 % at 30–45, 67 % beyond 45), the warden's head in 95 % (98, 100, 94, 85). From the deck rail alone: 26 % and 51 %.
- Machine record: one transient `DW1054` while the lookout stood as a stand-in (the gate tower's hatch seen across it), cleared when the lookout was detailed; no other code hit.
- Ladder on the round-3 build (manifest `1613e6dc31aec614fa4a0b8313dd6558867f0497ed146281e9fecc847e333e88`): bot critical path passed, 8 steps; `[pursuit] 3 pursued step(s) of 8, 1 pursuer(s), 34 reading(s); closest approach 14.97 block(s)`. Branch runs `world/0`–`world/2` ran and passed (closest approaches 15.01, 13.48, 13.79). PackTest: the same one red (the census test on a body of maximum health 1). Written world: the same `DW0955` on the four bell power cells. Staging gate: the same `doune-04` UNBOUND.
