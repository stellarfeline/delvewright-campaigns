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

## Branch chronicle (step 11)

The build writes 32 world chronicles (`validation/world-chronicle-<n>.md`, `validation/branch-plan.json`), one per assignment of the five binary threads: tail (nest / Dumpling), Founder (buoys / work-song), Loaf (oven / forge), chorus (done / not), curtain (done / not). Each was read end to end against `DESIGN.md` and against the flag-gated dialogue and epilogue lines reachable on it. A chronicle line is cited as `w<world>:<storyline item>`.

| claim reviewed (dialogue/design beat) | branch | chronicle line(s) | verdict |
|---|---|---|---|
| `dlg/play-dragon` #1 → `dlg/play-dragon-nest`; epilogue `opening-night` oc 0 (the jackdaw's nest) | `branch/nest-moved` | `agathe-tail#4` gains, w0–w15 items 7/12/16/21 | cleared (16 of 16 worlds, absent from the other 16) |
| `dlg/play-dragon` #2 → `dlg/play-dragon-dumpling`; epilogue oc 1 (Dumpling plays the tail) | `branch/dumpling-tail` | `agathe-tail#5` gains and `quests/1/on_complete/3` arrives, w16–w31 items 7/12/16/21 and 9/14/18/23 | cleared (16 of 16) |
| Dumpling stands on the square at the finale (design: only on the second branch) | `branch/dumpling-tail` | `quests/1/on_complete/3` arrives, w16–w31 only | cleared |
| `dlg/play-founder` #1 → buoys; epilogue oc 2 | founder buoys | `sanna-buoys#3` gains, w0–w7, w16–w23 | cleared (16 of 16) |
| `dlg/play-founder` #2 → work-song; epilogue oc 3 | founder song | `sanna-buoys#4` gains, w8–w15, w24–w31 | cleared (16 of 16) |
| `dlg/play-loaf` #1 → oven loaf; endings encore / curtain-call | `branch/oven-loaf` | `runa-forge#2` gains, w0–3, w8–11, w16–19, w24–27 | cleared (16 of 16) |
| `dlg/play-loaf` #2 → forge loaf; epilogue oc 10; `ending/no-ending` | `branch/forge-loaf` | `runa-forge#3` gains and `on_complete/13` loses, w4–7, w12–15, w20–23, w28–31 | cleared (16 of 16) |
| chorus on the square; epilogue oc 4 (the chorus sang) | `branch/chorus-sings` | `obj/find-sverre` gains item 7 and `quests/4/on_complete/3..6` arrive items 8–11, even worlds | cleared (16 of 16) |
| epilogue oc 5 (Fenna sang alone) | `branch/no-chorus` | no chorus line in odd worlds | cleared (16 of 16) |
| epilogue oc 6 (the new curtain hung) | curtain done | `obj/tell-elin` gains, w0,3,4,7,8,11,12,15,16,19,20,23,24,27,28,31 | cleared (16 of 16) |
| epilogue oc 7 (the old curtain) | curtain not done | no curtain line in the other 16 | cleared |
| `ending/encore` (oven, applause ≥ 2) | oven + chorus + curtain | `on_complete/11` gains, w0, w8, w16, w24 items 38/39 | cleared (4 of 4) |
| `ending/curtain-call` (oven, applause ≤ 1) | oven, at most one strand | `on_complete/12` gains, 12 worlds | cleared (12 of 12) |
| `ending/no-ending` (forge) | `branch/forge-loaf` | `on_complete/13` loses, 16 worlds | cleared (16 of 16) |

No finding: every flag-gated dialogue option and epilogue line is licensed by a chronicle line on exactly the worlds whose flags it requires, and every chronicle line is a beat `DESIGN.md` licenses on that branch.
