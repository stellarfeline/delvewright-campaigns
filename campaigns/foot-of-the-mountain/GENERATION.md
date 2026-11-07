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
- `DW0210` stopped the first build: the finale's `set-time` to the setting sun is judged at the night sky (4), and 5155 reachable walkable cells measured below light 3 (5100 in 309 regions of the island's ground outside every plot, 55 in 24 detailed places). The finale now plays at `{"daytime": 11867}`, the latest hour judged as day (`DESIGN.md`, *The hour*), and the two Scene 7 pictures are redrawn at it; the build measures 0 dark cells.
- `DW0430` on `node/flight-1` and `node/flight-5`, and `DW0450` on Bernt, are step 9's (below).
- The build that ships (manifest `e0e78f7e2533cfdec8d6c19a216c3dda5d66897d9a3d0863dc354f986f70e359`) exits 0: `DW0210` 0 dark of 111808; 4025 attached blocks held, 0 dropped; the pacing line measures 2380 blocks of route, about 40 minutes at the metrics table's rate, against `target_minutes` 150 — the rest of the evening is conversation, which the route does not measure. 394 s wall, 2.81 GB peak, macOS arm64.

## Showcase cameras (step 8b)

17 cameras, one per approved picture, each estimated from its picture and moved against the build's previews until the subject was in frame. Three were moved again on the build's refusals: `lighthouse-near` (lens in a wall), `from-the-castle` (`DW0956`, subject 166 blocks away past the 160-block view), `plan` (`DW0724`, lens above the build height). No camera states an `after`: the world after `obj/take-places` is the world at load block for block (`DW0721`).

The square now carries the stage (step 9), and the two Scene 7 cameras were drawn again against the build that ships without being moved: `stage-near` frames the stage's boards, lanterns and painted flats with the cathedral front behind them; `square-far-evening`, from the cathedral steps, frames the stage from its back across the benches. The two pictures disagree on which way the stage faces; the build follows the near picture.

## Detail (step 9)

Handouts are regenerable files under `.out/handouts/`. Wave bound as `allocation --all` printed it: `concurrency: 0 = min(0, max(1, 10 / 2))` (every place already carries a passing program); two authors ran at once for the two refused places.

| place | attempt | handout | tokens | duration | repaired | commit exit |
|---|---|---|---|---|---|---|
| `node/flight-1` | 1 | `.out/handouts/flight-1/handout-1.md` | 93329 | 626 s | `DW0430` | 3 (battery: `DW0430` on `node/flight-5`) |
| `node/flight-5` | 1 | `.out/handouts/flight-5/handout-1.md` | 117425 | 756 s | `DW0430` | 3 (battery: `DW0450` on `npc/bernt`) |

`DW0450`: Bernt's mark stood inside a stone mass of the castle piece; it moved to the clear side of the same anchor (`+[-3, 0, 0]`). Adjustments in this step: 2 bodies moved inside their plots (Dumpling, Bernt), 0 stations changed, 2 places re-authored.

A second pass repaired what steps 10 and 12 found on the build at `c13baa36…`. Each finding went into the place's node `note` (the stage, and the five doorways) and into its handout as the refusal (`--from`, a file stating the finding: the written world's cells, the threshold frames and the census entries, since `handout.py` writes no handout for a program `detail --check` passes). Wave bound as `allocation --all` printed it: `concurrency: 0 = min(0, max(1, 10 / 2))`; two authors ran at once.

| place | attempt | handout | tokens | duration | repaired | commit exit |
|---|---|---|---|---|---|---|
| `node/bakery` | 1 | `.out/handouts/bakery/handout-1.md` | 95462 | 110 s | `DW0955` | 0 |
| `node/cottages` | 1 | `.out/handouts/cottages/handout-1.md` | 80909 | 108 s | `DW0955` | 0 |
| `node/square` | 1 | `.out/handouts/square/handout-1.md` | 120892 | 394 s | `DW0845` (the stage) | 0 |
| `node/harbour` | 1 | `.out/handouts/harbour/handout-1.md` | 82448 | 74 s | `DW0955` | 0 |
| `node/weaver` | 1 | `.out/handouts/weaver/handout-1.md` | 90929 | 514 s | threshold read | 0 |
| `node/netloft` | 1 | `.out/handouts/netloft/handout-1.md` | 111043 | 925 s | threshold read | 0 |
| `node/townhall` | 1 | `.out/handouts/townhall/handout-1.md` | 82965 | 397 s | threshold read | 0 |
| `node/boatwright` | 1 | `.out/handouts/boatwright/handout-1.md` | 96376 | 507 s | threshold read | 0 |
| `node/carpenter` | 1 | `.out/handouts/carpenter/handout-1.md` | 106755 | 1017 s | threshold read | 0 |
| `node/weaver` | 2 | `.out/handouts/weaver/handout-2.md` | 83612 | 307 s | `DW0955` | 0 |
| `node/boatwright` | 2 | `.out/handouts/boatwright/handout-2.md` | 106792 | 596 s | threshold read | 0 |

Adjustments in this pass: 1 station added (`anchor/stage`, the square), 4 marks moved inside their plots (the square's `node-square` and `spawn`, the weaver's, the net-maker's, the boatwright's), 9 places re-authored, no shell changed.

## Ladder (step 10)

On the build at manifest `c13baa369261bf74f365ce69911ff077dea75371aab86d3ced17f4119c5c3bed`:

- PackTest exit 0.
- Bot critical path exit 0 (run timeout raised to 60 minutes for a walk the route measures at 40); `die-retry`, `death-loop` and `crush-death` have nothing to prove (no combat, no lethal volume, no crush gate).
- Branch runs: all 32 worlds selected (`DELVEWRIGHT_BRANCHES=all`); world/0 to world/2 PASSED (about 9 minutes a world) when the build machine was taken back mid-run; the rest ran on unobserved and their record is not read here. Step 10 is not complete until it is.
- The same campaign built on two hosts (Linux x86-64 release archive, macOS arm64 release archive) gives one manifest, `c13baa36…`.
- Written world: `DW0955`, 27 cells the server holds differently from the engine's model — 24 `dirt_path` the server turns to `dirt` (in `node/bakery` and `node/cottages`), 3 harbour stairs the server waterlogs at sea level. Every other class agrees. This is the engine's model, not the campaign.
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

## Visual review (step 12)

`delvec frames` on the build that ships (`e0e78f7e…`): `renderer: lumenwright 0.3.0, backend apple m2 pro (metal) (auto)`; 955 shots (634 POV, 190 interior, 116 threshold, 14 NPC, 1 spawn), 209 s wall, 3.04 GB peak.

- **Scene 7 against its pictures.** The square holds the stage the two pictures show: boards on trestles on its east half, lanterns along the front edge, painted flats at the back, rows of benches facing it on the west half, the well and the two trees kept. The near picture is answered; the far picture is answered from the stage's back (above, *Showcase cameras*).
- **The route between places.** The proven route still leaves the streets: from the square to the castle 204 of 424 route columns lie outside every place's box and only 21 on a way, and from the castle to the lighthouse 488 of 650 lie outside every box and none on a way (the thinned waypoints of `validation/critical-path-waypoints.json` against `delvec allocation --all`'s boxes). Cause, read in the engine at `delvec--v1.15.0`: the router is an A* over every standable cell of the assembled world (`crates/delvec/src/compiler/nav/route/mod.rs:129-196`, `find_path_avoiding`), whose step cost is one flat step plus 2 per sixteenth of height change (`crates/delvec/src/compiler/nav/world/body.rs:1348-1359`) and knows nothing of ways, so the terraced flanks the island's terrain lays outside every plot (1-block steps, walked by jump edges) are cheaper than the zig-zag road. The bot, the POV frames (`crates/delvec/src/compiler/emit/routes.rs:1118`) and every route proof walk that one route. A player is led by the compass, which points straight at the objective's place (`crates/delvec/src/compiler/emit/guidance.rs:1407-1416`, a `lodestone_tracker` target), and by the streets they see; nothing stands between the streets and the open ground, so a player who follows the needle crosses the same flanks. The fix is the terrain outside the plots (the site plan's ground, `terrain/island.png`) or the router, neither of which is a station or furnishing: not changed here.
- **Threshold read**, re-read on the 28 frames of the places this pass touched or that missed before: `threshold read: 28 frame(s), trade misses 18, front misses 0, thing misses 0, holding misses 0`. Repaired: weaver 3 (the loom first from the door), net loft 2 (the hull and the hung nets), guildhall 2 (the arcade's market), carpenter 2 (bench, log pile, plank stack). Still missed: boatwright 2 after two attempts (the shed frame shows a fire and a cauldron, the yard frame a block-built hull at a slant that does not read as a boat); cathedral 4 (the eye on the square stands before a buttress of the west front), inn 3 (a porch wall and window), potter 3 (a closed door and a wall of the house), harbour 3 (the harbourmaster's house corner stands between the quay crossing and the boats), lighthouse 3 (the cottage's side wall): each is the shell or the plot's arrangement facing the crossing, outside this pass. The square's threshold reads as a square (well, benches, stage).

## Toolchain

`/new-delve` plugin 1.15.0 (the skill pages at engine tag `delvec--v1.15.0`), engine release `delvec--v1.15.0`, `dsl_version` 0.69.0. The prefab library is this repository's own `prefabs/`; the shipped library was not taken.

## Hand-over (step 13)

The staging gate on the build at manifest `c13baa36…`, with the bot's run report and the written-world record: the findings ledger reads **STAGEABLE** (52 bound, 80 inapplicable, 27 declared uncoverable, 0 unbound); the gate refuses on one reason only, the written world (`DW0955`, 27 cells, the engine's model). Nothing is staged by this run.
