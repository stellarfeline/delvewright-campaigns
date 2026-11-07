# Curtain Up in Kelderby — generation record

## What the brief pinned, and what was invented

- Pinned: a cheerful RPG — warm, funny, low-stakes, a town worth living in — on the town at the foot of the mountain as built. The map is adjusted moderately at placement and never rebuilt.
- Invented: the town's name, the Founders' Play and its legend, the mistaken troupe, the cast, the web (one hub, three spokes, two optional strands, a finale) and three endings.
- Brainstormed with an outside model for ideas; every line here and in the documents is written for this campaign in English.

## Engine

- `dsl_version` 0.69.0, `delvec` 1.15.0 from the release archive `delvec--v1.15.0` (steps 8 on); steps 1 to 7 ran on the same version built from source before the release was published.

## Placement

- The map body is the town as built. Placement changed the layout graph only: `goal` from the quay to the square, `beats[]` bound to the eighteen planned objectives, `critical_path[]` re-derived as the mandatory walk through the spokes' places. No box, seam, piece or program changed.
- `world.json`: the title, theme, premise, `target_minutes` (150) and `time` (late afternoon) are this campaign's; `test_level` is dropped, because this is a campaign that owes a design record.

## Posture note

Three axes pushed off the default for this campaign: **address** — Hedda turns to the audience, the player, as if from the stage, and the curtain call breaks the fourth wall outright; **emotion** — Lady Agathe and Sanna name their fear in plain words instead of showing it; **plot shape and resolution** — two subplots with their own small endings, and one ending (`ending/no-ending`) where the play never reaches its last scene and the legend is left unsettled. Also off the default: the clerk who stands in the way is right.

## Names

Every named body is one character and one spelling. No wave and no actor shares a name in this plan.

## The design gate

Answered by the planner for the owner, who plays this delve without seeing its script: build this delve as written. The walkthrough it answered is the approved set under `design/`: three views of the whole town and a near and a far view of each of the seven scenes, seventeen images, every one drawn under the one style contract in `design/style.txt` and anchored on `reference/view1-from-the-sea`, each recorded in `design.json` with the sky it shows (fifteen late afternoon, two sunset, all clear).

## Content

- Every objective is the one `layout-graph.json`'s `beats[]` names; no beat was added or moved. The play itself is Hedda's dialogue on the square, so the finale keeps its two planned beats.
- The cast ledger reads the quests in file order, so a spoke's moves are already made for every quest declared after it; a body moved on a forked beat (Dumpling, the chorus) carries complementary per-branch placements in every quest. Post-spoke dialogue is gated on the spoke's `-done` flag, which every run sets.
- Four bodies that share a place's anchor stand at offsets from it (`npcs.json`): Bernt and Dumpling at the castle, Inga and Sanna at the lighthouse.

## Languages

`world.json` declares `zh-cn`. Its sidecar is written by the configured translation provider from the English documents.

The sidecar is not written yet: two runs of `i18n-translate.py` against the configured provider stopped on the first batch of 19 keys with no complete reply (at the default 120 s deadline, then at 400 s), while the provider's model listing answered at once. `validate` and `analyze` therefore carry one refusal, `DW0180`, until the provider answers and the sidecar is written by it.

## Build (step 8)

- `DW0307`: the happy ghast's two marks stood four courses in the air, where a `move-npc` walk can neither start nor end. Both marks now stand on the ground of the same plots (`npcs.json`, 15 cast and move offsets in `quests.json`).
- `DW0210` stops the build: the finale's `set-time` to the setting sun is judged at the night sky (4), and 5155 reachable walkable cells measure below light 3 — 5100 in 309 regions of the island's ground outside every plot, 55 in 24 detailed places. The town's light was placed and proven at noon. Under the late-afternoon world hour alone the same build measures 0 dark cells.
- `DW0430`, met on a scratch copy past the two above: 4 stair blocks in `node/flight-1` and `node/flight-5` on the proven route face away from the climb the route makes onto them. The repair is in those two places' programs.
- Steps 8b to 13 wait on a build that exits 0.
