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
