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

- **The map's reference** is five views under one style contract (`design/reference/style-contract.txt`), view 1 from the prompt alone and every later view chained on view 1: from above the coach road, a plan, a west elevation, the body from the Narrows, and from above the tail looking north. The plan view was drawn twice: the first return laid the body east-west, against the plan; the second, with the orientation stated, is the one kept. Reference images are style authority only; the geometry is `geometry-brief.json` and `site-plan.json`. The views stay drafts outside `design/` until the design gate: an image under `design/` is an approved image, and it owes a `design.json` row stating the sky it was approved under, which no one has given yet.
- **The body lies north-south, head to the north**, facing the town across the black water, with the Flank Ridge along its west side. `DESIGN.md` does not state the heading; this one puts the mouth at the Jaw Bank where the crossing lands and the flank wounds in sight from the ridge and, obliquely, from the Narrows.
- **Covered stairs.** A stair seam's opening has to lie inside both places' headroom, and a sky-open place claims only its size class's minimum headroom (a road six courses, a hall eight, an arena twelve). So every stair with a rise of eight is hosted in a roofed place: a covered flight of cliff steps between the coach road and the high street (a place `DESIGN.md` does not list), the harbour office, a covered fish market hall, the chapel crypt and the rope shed. The net lofts sit three courses above the seawall and the mast platform four above the launch's deck so that their open hosts can carry the stair.
- **The Run's descent is four broad steps.** Forty blocks from the back to the bank cannot be one open-air stair under that rule, so the back falls in four arenas of eight courses each (`back-upper`, `back-middle`, `back-lower`, `tail-flank`) to the bank behind the tail, which lengthens the tail beyond the brief's 140 blocks. Recorded as a capability limit, not a design choice.
- **No massif for the body.** A whole-owned volume may not contain a place, and the body's inside is places, so the blockout has no outer body mass. Its exterior shape is the sculpted form's (`delvec sculpt`), bound at step 13.
- **Two placement components**: the town and the flat (pinned at the coach road) and the far bank with the body (pinned at the far landing), joined only by the `carry` crossing and the two ferry bells.
- **Blockout lighting** (`lantern`, minimum 7) lights the derived massing for the walk only; detailed places carry their own placed light.

## Step 3 — the story documents

- **NPCs**: the four of `DESIGN.md`, each with one job. Wenna, Tregear and Marrack are `quest-giver`, Davey `flavor`. Davey stands by the heart from world load: the party first reaches him there, so he needs no deferred entrance. Each body is a `minecraft:mannequin`; the skins `DESIGN.md` asks for are made with the skin toolchain at step 5, so no `skin` is declared yet.
- **Classes**: the four kits of `DESIGN.md`, nothing added. The Physician's splash potions carry `minecraft:healing`; the Scholar's brush is named "Scholar's Brush" and is in no other kit. No bonfire, so no flask.
- **Quest plan**: the sixteen quests of `DESIGN.md`'s outline in one chain, all mandatory, finale `quest/the-pier`; one branch point at the pier, forking on `flag/stone-kept` and `flag/stone-returned` to `ending/the-keeping` and `ending/the-return`. `min_players` stays 1.
- **Where step 3 ends**: `validate` carries only refusals whose messages name something stage 5 or 6 supplies — DW0816 ×36, DW0817 ×9 (every one "not open yet"), DW0818 ×13, DW0934 ×4, DW0930 ×2, DW0152 ×4, DW0172 ×2, DW0112 ×2, DW0482 ×2, DW0150 — plus the standing DW0813 and DW0822 warnings. DW0822 projects about 40 minutes of walking against the 150-minute target; the rest of the time is the beats.

## Step 4 — the design gate (prepared, not approved)

- The walkthrough holds the five map views and 38 scenes (the 36 places of `DESIGN.md` and the two endings' dawns), each with a near and a far view, every image labelled with the `time` and `weather` tokens it is declared under: `night` + `clear` for 74 images, `dawn` + `clear` and `dawn` + `rain` for the two endings. The painted skies (the wrong place, the inside of the body, the red night, the sea fog) are atmospheres under those tokens, named under each image.
- Every scene is anchored on map view 1 under the same style contract. The first pass chained every call on view 1's interaction; eighteen far views came back as copies of view 1's framing or against the design, and were drawn a second time anchored on view 1's image (`--style-ref`) with the camera stated. Two views broke the contract or the design on both draws (readable lettering on the customs chart; the ferry house open to the sky) and are shown with both draws and the fault named.
- Inside the body the light follows `docs/reference/interior-lighting.md` §7 of the engine (sources embedded in the walls and the vault, artificial sources hidden), which answers `DESIGN.md`'s open light question for the pictures; it is still owed a demo level.
- The images are drafts in the gitignored `.refimg/stranding/gate/` until the user approves them; nothing is in `design/` and there is no `design.json`.

## Conformance against `DESIGN.md` at the gate

Deviations the run made, none requested, each forced or a gap-fill: the covered cliff steps (a place `DESIGN.md` does not list), the covered fish market hall, the net lofts three courses up and the mast platform four, the quay at y 72 rather than 66, the Narrows four blocks wide on the kit grid rather than three, the body's heading (head north) chosen where `DESIGN.md` is silent, the back descending in four broad steps that lengthen the tail past 140 blocks, and no body mass in the blockout until the sculpted form is bound at step 13.

## Step 4 — decisions taken for the delegated review

The review of the act 2–4 and ending images found three things `DESIGN.md` did not decide; each is now decided there (English and zh-cn) and the images are drawn to it:

- **The wrong place stands over the body's bank and outside until the cut.** `DESIGN.md` made the whole flat the wrong place and was silent on the bank; for continuity the far landing, the Flank Ridge, the Jaw Bank, the back and the Crown stand under `atmosphere/wrong-place` from the first tick until the cut at the Brow, then under `atmosphere/red-night`. The site plan still carries the wrong place on the flat's boxes only: carried on the bank's boxes, its paint would meet the inside-body boxes' paint at the mouth and the breach, which the build refuses (`DW0929`), so whether the bank carries it with a gap or is painted by a beat is settled with the beats at step 5.
- **One body.** The Fathomer has one silhouette, `DESIGN.md` § The body, in the stranded-creature language of the demo level The Beached Thing (head and dropped jaw on the mud, shoulder, spine ridge, ribs at the wounds, flippers, a long tail ending in flat flukes; hide, bone and flesh tones), with this campaign's own parts added: the Brow Stone in the forehead, the blowhole, three flank wounds.
- **The inside's light** follows the engine's `interior-lighting.md` §7 and the owner's lighting rules: natural light set into the walls and vault, artificial sources hidden, placement staggered in three dimensions, the upper space lit. The comparison of soul lanterns and crying obsidian stays with The Beached Thing.
- The Pier image is drawn to what `DESIGN.md` says happens there: one player holds the Brow Stone before Wenna, Davey and Tregear.

## Design additions before step 5

- **The approved design** is in `design/` (81 images) with `design/README.md` naming the set and its known flaws, and `design.json` holding one row per image.
- **The body is a realistic rotting sperm whale** (`DESIGN.md` § The body), replacing the generic leviathan the concept images drew. Tentacles rising from its wounds are the wrongness and are not the whale's. The approved images stand as style; where they differ from § The body, the record wins. The sculpted form is bound at step 13, after the walk.
- **The escape crossing is the climax reveal** (cutscene 10): the skiff out on a separate patch of open sea in fog and storm, the camera rising toward a vast shape, a lightning strike and a fog flash showing a colossal figure, then the landing in the near ferry house. Played once.
- **The return is the bad ending**: by what it shows (the stone back in the sea, Wrackham under water on its bottom row) it reads as the bad one, and the same figure rises at the town's shore at its end. No player text labels either ending.
- **Both figures wait on engine work** (the demo level The Thing Beyond the Fog, spec-0092: lightning at a mark, a timed fog flash, an open-backed sculpt form, glowing eyes). Authored now: the crossing link, the fog, the shots over open sea, the landing, and the return's shots. Marked placeholders: the figure, the lightning and the fog flash. The thunderstorm is part of the placeholder too: no approved image is drawn under `thunder`, and `DW0890` holds the world's reachable skies to the approved rows, so the weather is set with the capability and the image that shows it.

## Steps 5 to 8b

- **Stage 5 and 6** are written by one generator so ids, flags and anchors are spelled once: sixteen quests with a cast ledger each, six waves, three watcher actors, twelve tentacle assemblies, nine runtime data, twenty-odd triggers (the valves, the tentacle hit counts, the skiff tiller links and the two ferry bells, the sealed-door answers), and dialogue for the four characters, a second body for Davey once he is home (one character, two declarations, one spelling), and four sleepers with a bark pool. Every objective is bound to its place in the layout graph's `beats[]`.
- **The Chinese** is the `zh-cn` sidecar transcreated by `tools/creator/i18n-translate.py` (deepseek-v4-pro), 441 keys, every line accepted by its fact check. The tool's own closing validate fails in a content clone, where the library is `prefabs/` and not `campaigns/prefabs`: it calls `delvec` without `--prefabs`. The sidecar validates when `delvec` is given the library.
- **Skins** for the four characters from the skin toolchain (`skins/cast.json`). **Textures**, drawn for this campaign: the Drowned as fish-folk and their outer layer, the louse, and the red moon on the waning gibbous phase, which the cut advances to with `set-time` (the design rows of the four after-cut scenes state that sky).
- **The tentacle rig** (`prefabs/rigs/tentacle/rig.json`) is written by the engine's own `prefabs/rig-generator` at `delvec--v1.8.1`, byte-identical to the rig on the pit demo's branch. The content library at its pinned revision has no rig, and the page names no step that produces one.
- **The site plan grew** five mud places beside the way (the sinking stages clear them) and the Narrows shelf the first tentacle strikes: a clear or a blow is an anchor-centred box, so the thing cleared or struck needs a place of its own off the way.
- **Build**: `delvec build` exits 0. Hashes: site plan `47bb3e57…`, layout graph `aa13434b…`, blockout `40174164…`, engine `ff6bd492` (delvec 1.8.1). Pacing measures 2970 blocks of route, about 50 minutes of walking, against 150 targeted; the rest of the budget is the fights, the dialogue and the twelve cutscenes, and it is the walk that judges it.
- **Showcase cameras**: 81, one per approved image, estimated from the pictures and the plan's coordinates and checked with `delvec cameras --preview`; three lenses that clipped a block were moved. Against a blockout most frames show massing, not the picture; they are re-placed when the places are detailed, or by hand in the game.

## What 1.8.1 could not carry, and what was authored instead

- **The Scholar's reading** of the carvers' script: `DW0849` refuses an objective only one class can complete when its item is in only that class's kit. The script answers everyone with "nobody here can read it"; the Scholar-only line is not in the campaign.
- **The endless Throat**: a loop needs a jogged, roofed hall whose view closes inside one period (`DW0947`), and the blockout's Throat is a straight corridor. The Throat is a corridor with the wrong rib to break; the loop comes with the Throat's detailed piece at step 13.
- **The Run's killing volumes and the Stomach pool**: a staged lethal volume must sit three courses under a rim; the blockout's holes are two courses over the sea. The bank still falls behind the party; the kill volumes come with the detailed pieces.
- **Tentacles that strike** beside the way at the Jaw Bank, in the Rib Cathedral, on the Crown and on the Run: a blow is a box centred on an anchor, so every striking tentacle needs a place of its own to land in. The Narrows tentacle strikes its shelf; the others can be struck down and retract, and do not strike back yet. The flank-wound tentacles stand at the ridge's edge, not in the wounds, because a mark may not leave its place.
- **Tentacles rising**: a hitbox is judged against the spawn frame, and a tentacle spawned rising is underground; they spawn standing.
- **Darkness and blindness** in the perception bundles: refused within reach of a drop (`DW0943`); the bundles use nausea, the face particle and sound.
- **The watcher** stands at a fixed facing and vanishes or moves when approached; no body turns to follow a player.
- **The far tiller's line before the Run**: a party trigger is visited by the critical path whenever it is live, so the tiller is gated on the Run and says nothing before it.
- **The stake lamps** lit by the lighthouse are told, not set: the lamp posts are detail, and a `set-block` needs an anchor at each post.
- **The view distance** the far views need (the body from the coach road, the lamps from the gallery, the town from the Crown): spec-0091. **Pictures of the world after a beat** for the after-beat cameras: spec-0089. **The figure beyond the fog**, its lightning, the fog flash and the storm: spec-0092 (placeholders in cutscenes 10 and 12).
- **An engine emission defect**: a presser `use` trigger with a trigger-level flag gate emits an `execute` the 1.21.11 command tree refuses ("matches 1run" with no space). The valve triggers carry their gates on their effects instead, which is the DSL's own `when`.

## Step 9 — the walk

**Passed.** The route reads, and the walk found no design problem; the walker stopped there, so the walk is over. What it met were technical faults, and round 2 answers them (engine `delvec 1.8.2`, dsl 0.35.1, built on the same blockout `40174164…`):

- **A design ruling** for this campaign: no objective or waypoint text and no reach steps; progress comes from reading, talking, using and taking (`DESIGN.md`, *Guidance and writing*). Every reach objective became a reading, a conversation, a use or a taking; arrivals that start something are approach triggers. The engine forces three things against it, recorded as gaps below.
- **Change narration** is cut everywhere ("the way behind you narrows" and its kind); the changes that carry the story keep the cutscenes they already had (the first creep, the lamps, the first view, the mouth, the beat stopping, the Crown, the cut, the crossings, the endings). No new close-up was needed.
- **The tentacle hit one fixed spot**: authoring — the strike had no `aim`. It now turns to the nearest player among 8 facings inside an arming region kept to the shelf side (the engine turns a blow to a facing; it does not track a player). **The retract looked wrong**: the emitted retract is the pit demo's, function for function; what differs is that a strike pattern begins its next wind-up over a played clip while anyone stands in the arming region. The striking tentacle now sinks through a non-striking twin spawned on its retract.
- **The watcher did not vanish**: authoring — the street trigger was centred twenty blocks from the watcher, and both approach triggers could fire while the party watched the opening camera fly through. Each watcher now stands on its place's anchor, vanishes within a few blocks of it, and is armed only after the opening cutscene.
- **The crossing did not carry the walker**: authoring — the teleport took one cell of the skiff, and the cutscene returns every player to where the presser stood, so anyone a step off that cell stayed on the stage; sneaking only frees the camera and changes nothing. The seat is now a five-cell row across the skiff. **The bell was missing**: authoring — a trigger on an empty anchor is an invisible box; the bells and tillers are now real blocks.
- **Name plates on the Drowned**: authoring — the wave mobs were named; the names are gone. **The Drowned's head band**: the outer layer in 1.21.11 uses the base UV, so the old outer image drew nothing; the band was the base face's wide dark mouth row. The face is redrawn and the outer layer is transparent. Only a look in the game confirms a mob texture.

## What round 2 could not carry, and why

- **A fight cannot be an objective without text**: an untitled `kill` is refused (`DW0863`: "carries neither a `title` nor a `hint` … Give `<id>` both a `title` and a `hint` saying where the wave arrives"). The fights are now spawned by quest beats and are not objectives; `DW0380` warns that the hull fight has no bypass, and the staging gate is red on ledger row `bell-14`, whose check binds only to `kill` objectives.
- **Every interact objective shows a glowing marker**: `activate_o_<obj>` emits `summon minecraft:item_display … {Glowing:1b,…,item:{id:"minecraft:lantern"}}` for every interact, titled or not, and nothing turns it off. It is a waypoint the ruling does not want.
- **A wave spawned from a trigger is not placed**: `DW0310` ("its spawn anchor is not placed in any assembled area") refuses a `spawn-wave` an approach trigger fires, so a fight starts on a quest beat, not on arrival.
- **A checkpoint set from an approach trigger** strands the route proof (`DW0315` named a coach-stop anchor after a far-landing checkpoint); checkpoints are set by objectives, so the Run has its landing checkpoint and none on the back or the bank.
- **A talk beat that must follow another** meets the `DW0205`/`DW0191` pair: an ungated completing button is refused for being early, a gated one for being gated. The homecoming is a use at the pier end instead of a word with Wenna.

## Step 10 — the machine ladder (round 2): red on two engine defects

- **A rebuild leaves the last build's files behind.** `delvec build -o <dir>` writes every emitted file and removes none (`write_output` in `crates/delvec/src/main.rs`), so the reused `validation/delve-output` carried 134 files the current build does not emit — the removed objectives' functions, their PackTests (`verb_kill` asserting `dw.o_the_slipway_drowned`), and live advancements (`c_the_spade.json`, `press_pillar_script.json`). A build into an empty directory is byte-identical to the current emission; the output directory is now cleared before every build here.
- **PackTest: the atmosphere tests share the world.** The generated `atmosphere_repaint_<n>` tests paint and read biomes at absolute coordinates and run in parallel batches of 50; one test's "kept" cell lies inside another's repaint box (`atmosphere_repaint_1` reads `162 74 130`, inside `atmosphere_repaint_4`'s `[142,52,123]..[173,87,154]`). Two runs of one build failed different sets: `atmosphere_repaint_5`, `atmosphere_places`; then `atmosphere_repaint_1/2/3/5`, `atmosphere_places`, `v06_damage`. An intermittent red is an under-specified test; it is not re-run and the campaign's paint is not moved to dodge it.
- **Bot: a cutscene inside a `sequence` is not waited out.** `cutscene_seconds_in` (`crates/delvec/src/compiler/plan.rs`) reads only top-level `cutscene` effects, so the notice step, whose completion runs the opening cutscene from a `sequence` step, carries no `cutscene_seconds`; the bot walks its next leg while in spectator and is stranded at the first camera (`step 2 (talk-to) failed … bot at [177.5, 94.3, 655.4]`). A cutscene fired by an approach trigger is invisible to the plan the same way (the first run: `step 1 (interact) failed … bot at [177.5, 92.9, 637.4]`); the route's arrival cutscenes now play on the objectives beside them (the notice, the pillars, the chalk arrow) and the Crown's arrival shot is cut.
- Not run past the first red: the die-retry and death-loop stages report unbound (the campaign has no mandatory combat and no lethal volume), and the branch runs wait for a green critical path.

## Step 11 — the branch chronicle

Branches `branch/the-keeping` and `branch/the-return`; the two chronicles are identical to line 120 and differ only at the choice (line 122) and the ending (line 124). No dialogue node is flag-gated; every node is reachable on both branches, and the campaign ends at the choice.

| claim reviewed (dialogue/design beat) | branch | chronicle line(s) | verdict |
|---|---|---|---|
| Davey by the heart, "It's dreaming, and we dream it…" (`dlg/davey-dream`) | both | 91 `learns` (still dreaming) | cleared |
| Davey in the skiff, "I don't remember any of it. Is my mother all right?" (`dlg/davey-awake`) | both | 93 `opens` (Davey wakes), 99 `arrives` (to the skiff), 110 `survives` | cleared |
| Davey on the pier, "Mother says you came a long way for me." (`dlg/davey-home`) | both | 116 `arrives` (home on the pier) | cleared |
| Wenna on the pier offers the choice (`dlg/wenna-pier`) | both | 105 `arrives` (Wenna to the pier), 107 `arrives` (Tregear), 116 | cleared |
| Marrack, "I took two men in…" (`dlg/marrack-boy`) and the shore of the pool | both | 66 `learns`, 85 `learns` | cleared |
| The keeping: "Tregear does not sleep: under his chapel the stone dreams" | `branch/the-keeping` | 122 `believes` (to Tregear), 124 `survives` | cleared |
| The return: "Nobody in Wrackham dreams." | `branch/the-return` | 122 `believes` (into the sea), 124 `seals` | cleared |
| DESIGN.md: Davey goes ahead along the causeway to the pier | both | 114 `departs`, 116 `arrives` | cleared — he goes to his mother when the party reaches the pier end |
| DESIGN.md: the keeping ends at dawn, the town clear | `branch/the-keeping` | 124 | cleared |
| DESIGN.md: the return shows the bottom row and the figure at the shore | `branch/the-return` | 124 | cleared for what is built; the figure and the bottom row wait on spec-0092 |

One contradiction found and fixed before this table: line 91 read "Davey, awake, speaks the dream's words" two lines before "Davey wakes".

## Round 3 — the owner's rulings (content issue 168), on the released engine

Toolchain: engine release `delvec--v1.8.2` (commit `11cd7c8a73b4b3b9c2383e67310ba6d49fc19903`), binary `delvec 1.8.2, dsl 0.35.1, mc 1.21.11`; the `/new-delve` page's pin check (I1b) exits 0 against it. Prefab library: this clone's `prefabs/`.

- **The journal** restates what the story has told: seventeen objectives carry a title (twelve a hint), each naming only what a person or a reading has said by then; objectives nothing has told stay untitled. Wenna's hire now says where to go (the chapel past the fish market, the Customs House key), and Marrack's says the road runs past the pillars and the Narrows to the ferry house.
- **Props**: fourteen of the sixteen interact objectives sit on a prop block, which the 1.8.2 emitter places instead of the glowing lantern marker (`activate_o_*`: `setblock` and no `item_display`). The lighthouse lamp is lit by the beat that lights it; the Brow Stone's block leaves the socket empty when it is cut.
- **The story frame and the endings**: the notice and Wenna say the party came to find out what is happening and stop it before it gets worse; the return's closing line says plainly that the catastrophe was not averted. The Figure is unnamed, mentioned obliquely, and never by the townsfolk.
- **The man at the oars**: Marrack rows. The launch body leaves when the pillars are read and two more declarations of him (`npc/marrack-near`, `npc/marrack-far`, one skin seed) sit at the oars of each copy of the skiff, forward of the seat row, so the carry never moves him. After the crossing back (`flag/reveal-seen`) his talk opens on a repeatable exchange.
- **Crossings**: the outbound crossing is one shot from the jetty out toward the far sea, then the carry; the crossing back plays its placeholder reveal once (the two in-house shots are gone: they framed an empty skiff), and any later press is an ordinary crossing.
- **Writing**: Davey's line about the valves says plainly what the right valve is; no line narrates the heartbeat; every line addressed to the party reads right for one player or four.
- **zh-cn**: 88 rows transcreated by `tools/creator/i18n-translate.py` (deepseek-v4-pro), then a review pass over the whole sidecar: one rendering per name (额石, 探海者, 温娜, 特雷加尔, 剥鲸铲, 溺亡者, 朝圣者之路, 窄口, 小艇, 打捞船, 渡屋, 山脊), no 你们 aimed at the party, and two meaning errors fixed (the flat read as an apartment; the launch read as the only boat that can sail out).
- **Waits on the unreleased engine** (DESIGN.md, *Waiting on the engine*): the Figure, the lightning and the party's stand-ins in the reveal; the obfuscated line; a visible press object for every `use` trigger, and for the Customs House lock and the diaphragm; progress that does not hang on reading an object; tentacle lock, re-arm and perception range; the walk after detail.
- **The walk record is stale**: `delvec allocation` refuses with `DW0841` because `walk-record.json` names layout graph `aa13434b…` and the graph now hashes `5ee5d3b4…` (round 2 changed the graph after the walk). Detail, and so the boats, cannot start until the blockout is walked again.

### Round 3 — the branch chronicle, re-read

The chronicles moved by six lines (the oarsman's three beats); both are identical to line 126 and differ only at the choice (line 128) and the ending (line 130). Claims this round changed or added:

| claim reviewed (dialogue/design beat) | branch | chronicle line(s) | verdict |
|---|---|---|---|
| Marrack rows the party across (`dlg/marrack-skiff`) | both | 64, 66 `learns`; 70 `departs` (the launch); 72, 74 `arrives` (the two oarsmen) | cleared |
| Davey by the heart says which valve is right (`dlg/davey-dream`) | both | 97 `learns`, 99 `opens` | cleared |
| Marrack ashore after the crossing back, repeatable (`dlg/marrack-ashore`) | both | not dated: side dialogue with no objective, gated by `flag/reveal-seen` from the crossing trigger (139–143, undated `seals`) | cleared — the chronicle dates no side dialogue |
| The keeping: "nothing comes up out of the sea" | `branch/the-keeping` | 128 `believes`, 130 `survives` | cleared |
| The return: "what it kept asleep wakes … no Wrackham left" | `branch/the-return` | 128 `believes`, 130 `seals` | cleared for what is built; the rising itself waits on the Figure |

### Round 3 — the machine ladder (delvec 1.8.2, project `dw-stranding-r3w`)

- **Build**: exit 0 into an empty directory; validate and analyze exit 0.
- **PackTest**: 269 tests, 6 failed — `atmosphere_repaint_1/2/3/5`, `atmosphere_places`, `v06_damage`: the same set as round 2's second run, the released engine's atmosphere proofs reading each other's paint in a shared batch. Not re-run.
- **Bot**: red at step 2, stranded at the first camera (`bot at [177.5, 94.0, 655.4]`), the released engine's plan not waiting out a cutscene inside a `sequence`, as in round 2.
- **Staging gate**: REFUSED, 1 of 122 — `bell-14` UNBOUND (no `kill` objective; 6 waves declared), as in round 2. 66 bound, 25 declared uncoverable, 30 out of stage.

## Round 4 — fights the story has announced become titled objectives, on the released engine

Toolchain as round 3: `delvec--v1.8.2` (`11cd7c8a73b4b3b9c2383e67310ba6d49fc19903`), this clone's `prefabs/`.

- **The fish-market wave is an objective**: `obj/the-slipway-drowned`, a `kill` on `wave/drowned-slipway`, first in `quest/the-fish-market`, bound to `node/fish-market` in `beats[]`. Its title and hint restate Wenna's warning in `dlg/wenna-start` and nothing more; the hint moved to it from the slate. zh-cn: 击退鱼市里的溺亡者, the hint carried with its key.
- **The other five waves stay untitled beats.** No line names the fight among the hulls, the two out of the wrecks, the lice, or the two by the pool before it starts; under the journal ruling they carry no title, and `DW0863` refuses a `kill` without one, so they cannot be objectives.
- **`DW0380` on `wave/drowned-hulls` stays.** Its own prescriptions are a real objective (refused above), or moving the wave off the walk / widening the boatyard, which is a placement decision this round was not given.
- **The layout graph changed** (one beat), so the walk record is stale by one more edit; `DW0841` already refused allocation since round 2.

### Round 4 — the branch chronicle, re-read

Each chronicle gains two lines (the `dies` beat and its subject), so round 3's citations past line 22 move by two: identical to line 128, the choice at line 130, the ending at line 132.

| claim reviewed (dialogue/design beat) | branch | chronicle line(s) | verdict |
|---|---|---|---|
| Wenna: the Drowned come up the slipway into the market (`dlg/wenna-start`), restated by `obj/the-slipway-drowned` | both | 20 `arrives` (the wave), 23 `dies` | cleared |

### Round 4 — the machine ladder (delvec 1.8.2, project `dw-stranding-r4w`)

- **validate / analyze / build**: exit 0, built into an empty directory. Promise line: 25 objectives, 1 `kill` (`DW0863`); round 3 had 24 and 0. Warnings unchanged: `DW0351` x5, `DW0379` x3, `DW0380` x1, `DW0781`, `DW0813`, `DW0821` x3, `DW0822` x2.
- **PackTest**: 271 tests, 6 failed — `atmosphere_repaint_1/2/3/5`, `atmosphere_places`, `v06_damage`, the set round 3 recorded (the released engine's atmosphere proofs reading each other's paint). The two new tests, `verb_kill` and `verb_kill_uncredited`, pass. Not re-run.
- **Bot**: red at step 2 as in round 3 (`bot at [177.5, 94.3, 655.4]`, the cutscene inside a `sequence`). The fish-market fight is step 3, so the muster reads `not-reached` and die-retry is UNBOUND (0 scripted deaths of 1 declared encounter): the run never reached it.
- **Staging gate**: stageable, 122 of 122 — 67 bound, 25 declared uncoverable, 30 out of stage. `bell-14` is BOUND (1 `kill` objective) where rounds 2 and 3 were UNBOUND.
