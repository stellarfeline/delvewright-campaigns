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

On the build that ships, manifest `e0e78f7e2533cfdec8d6c19a216c3dda5d66897d9a3d0863dc354f986f70e359`:

- PackTest exit 0: 96 of 96 required tests passed (137 s wall, macOS arm64).
- Bot critical path exit 0: 13 steps PASSED, 4 advisory findings; 14 watchers, 9 within reach on the proven path and asserted; `die-retry`, `death-loop` and `crush-death` have nothing to prove (no combat, no lethal volume, no crush gate). Run timeout 60 minutes; 438 s wall.
- Branch runs: all 32 worlds selected and run, each in a fresh world, every run report naming this manifest: **32 of 32 PASSED**, the endings each world's chronicle predicts reached (encore 4, curtain call 12, no ending 16). World 0 to 15 ran on the Linux x86-64 build machine on a byte copy of this build tree (896 files, same manifest), worlds 16 to 31 on macOS arm64 (8725 s for the sixteen).
- Written world exit 0: `model` 0 differing cells of 5038456 compared (from 27 on the previous build: 24 dirt paths under a block in the bakery, the cottages and the weaver's yard, 3 harbour stairs in sea cells); every other class is the server's physics or clock (random-tick 213, re-derived 28888); objects 236 block entities and 28 entities, each the server's.
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

The staging gate on the build at manifest `e0e78f7e…`, with the bot's run report and the written-world record: **STAGEABLE**, admitted with no override (`red_count` 0; 53 bound, 79 inapplicable, 27 declared uncoverable, 0 unbound). Nothing is staged by this run. The quest documents did not change, so the chronicle table above stands; the 32 chronicles this build writes cite the same items. The storybook's square picture is redrawn from its camera on this build.

## Round 2 (after the first playtest)

What the owner met, and what changed, structure only:

- **The spokes ran in no order at all.** The five act-2 quests open together when the hub completes, and the cast dispatch lets the last-ranked open quest's clause win; `"unchanged"` lowers to an ungated clause carrying the previous clause's scene. On the owner's world (checkpoint `02`, hub complete) the steward, the castle's lady, the baker and the lighthouse keeper each opened a bark pool or a post-quest root: no mandatory spoke's next step could be pressed. Every quest after the hub now declares each NPC's whole ledger as a partition over flags, with no `"unchanged"`; the four moves that cross spokes are gated on their quest's completion flag. The dialogue mask already orders each spoke's steps. `dialogue.json` is unchanged.
- **Faces.** 13 player-model skins composed from the cast section's briefs (`skins/cast.json`); the ghast keeps its own body.
- **The climb.** Four small places stand one ring cell off four level legs of the castle road (a spring, a bee garden, a herder's hut, a lookout), each authored by its own agent from its handout (attempt 1 each, `.out/handouts/poi-*/handout-1.md`; `handout.py` taken from engine `main` @ f2b106d09). The four road legs that gained a seam were re-drawn by their own generator; no road box moved.

| place | attempt | handout | tokens | duration | repaired | commit exit |
|---|---|---|---|---|---|---|
| `node/poi-spring` | 1 | `.out/handouts/poi-spring/handout-1.md` | 132854 | 478 s | — | 0 (`detail --all`) |
| `node/poi-bees` | 1 | `.out/handouts/poi-bees/handout-1.md` | 151214 | 625 s | — | 0 (`detail --all`) |
| `node/poi-hut` | 1 | `.out/handouts/poi-hut/handout-1.md` | 146763 | 561 s | — | 0 (`detail --all`) |
| `node/poi-lookout` | 1 | `.out/handouts/poi-lookout/handout-1.md` | 155828 | 506 s | — | 0 (`detail --all`) |

Wave bound as `allocation --all` printed it: `concurrency: 4 = min(4, max(1, 10 / 2))`; two authors ran at once.

On the build that ships, manifest `a0f583083c4c2de725be6cda7b115819a1107fe605e07ed69c61b4dfa527207f` (built twice, on the macOS arm64 machine and on the Linux x86-64 build machine: the same manifest):

- PackTest exit 0 (121 s wall). Bot critical path exit 0: 13 steps PASSED, 4 advisory findings (574 s wall). Written world exit 0, verdict pass, 5038505 cells compared.
- Branch runs: all 32 worlds selected, each in a fresh world, in three parallel tiers on the Linux x86-64 build machine: **32 of 32 PASSED** (tiers 1:41:12, 1:48:25, 1:29:19 wall); the endings each world predicts reached (encore 4, curtain call 12, no ending 16).
- Several players at once: five bots in one world, each on its own line from the hub (the three spokes and the two strands), started together: every line step of every bot passed; each bot stopped at its closing `assert-complete`, the finale being no line's step (161 s wall).
- The 32 world chronicles are byte-identical to the previous build's, so the step 11 table stands.
- Visual review of the four new places, one frame each from outside: each reads as what it is at playable scale.
- Staging gate: **STAGEABLE**, admitted with no override (`red_count` 0; 78 of 159 classes inapplicable).

## Round 3 (the quests rewritten so the town is played, not walked)

The owner played the previous version to an ending in about twenty minutes and found every line the same: walk to a place, talk, walk on. The map, the cast and their faces stay; the quests, their dialogue and the side content are re-authored from step 3, on the skill pages at engine `main` @ 71536aeb3 against the released `delvec` 1.15.0.

### Research: a town's quest content (round 3)

The question: what fills a hub town with play when nobody fights, and how much of it a two-to-three-hour evening needs. Each rule below says whether it is **cited** (a source says it) or **authored** (this campaign's own judgement from the cited material). The sources are design writing and published talks; none is a licensed asset, and nothing here takes their content, names or quests.

#### Sources

- [S1] J. Doran and I. Parberry, "A Prototype Quest Generator Based on a Structural Analysis of Quests from Four MMORPGs", PCGames 2011 — https://ianparberry.com/pubs/pcg2011.pdf (read: Tables 1–4).
- [S2] J. Alexander, "The Three Clue Rule", The Alexandrian — https://thealexandrian.net/wordpress/1101/roleplaying-games/three-clue-rule-part-3-the-three-clue-rule ; and "Running Mysteries: The Two Types of Leads" — https://thealexandrian.net/wordpress/50095/roleplaying-games/running-mysteries-the-two-types-of-leads
- [S3] H. Smith and M. Worch, "What Happened Here? Environmental Storytelling", GDC 2010 — https://gdcvault.com/play/1012647/What-Happened-Here-Environmental
- [S4] W. Spector, "Postmortem: Ion Storm's Deus Ex", Game Developer — https://www.gamedeveloper.com/view/feature/131523/postmortem_ion_storms_deus_ex.php ; and the GDC 2017 Classic Game Postmortem — https://gdcvault.com/play/1024338/Classic-Game-Postmortem-Deus-Ex
- [S5] PC Gamer, "Larian gave Baldur's Gate 3 its acclaimed reactivity by approaching it as 'weird Dungeon Masters'" — https://pcgamer.com/games/rpg/larian-gave-baldurs-gate-3-its-acclaimed-reactivity-by-approaching-it-as-weird-dungeon-masters ; and "Larian boss says we should think of Baldur's Gate 3's entire first act as the tutorial" — https://pcgamer.com/larian-boss-says-we-should-think-of-baldurs-gate-3s-entire-first-act-as-the-tutorial (press accounts of interviews; the transcripts were not read).
- [S6] The Escapist, Fallout: New Vegas reputation interview (Sawyer) — https://www.escapistmagazine.com/?p=76707 ; and the community record of the Fame/Infamy mechanics — https://fallout-archive.fandom.com/wiki/Fallout:_New_Vegas_reputations
- [S7] "Adding life to worlds with dialogue barks", Game Developer — https://www.gamedeveloper.com/design/adding-life-to-worlds-with-dialogue-barks ; E. Ruskin, "AI-driven Dynamic Dialog through Fuzzy Pattern Matching", GDC 2012 (summary: https://emshort.blog/tag/valve/).
- [S8] The engine's own `docs/reference/web-narrative.md` (§3, §4), for the hub, the spokes and endings that read the run.

#### What the sources say

- **A quest is a sequence of atomic actions, and a town's quests differ by which actions they are made of** (cited, S1): over 750 quests from four games reduce to nine NPC motivations, each served by a few strategies, each a short sequence of atomic actions — goto, get, give, listen, report, use, repair, exchange, spy, steal, damage, escort. A talk-only line is the strategy "goto, listen, goto, report" repeated; S1's own table carries it only under Knowledge ("Interview NPC") and Serenity ("Check on NPC").
- **Without combat the action set is get, give, use, repair, exchange, listen, spy and goto** (authored, from S1 Table 4 with the damage, kill, defend and escort actions struck out).
- **An investigation wants at least three clues to each conclusion it needs, because a player misses, ignores or misreads them** (cited, S2); **and a problem the adventure needs solved wants at least three solutions** (cited, S2, the chokepoint extension).
- **One problem with several solutions, each with its own consequence later** (cited, S4: "problems, not puzzles"; every problem several solutions; the further course reflects which was taken). **Larian's "n+1": a solution for the player who broke everything** (cited, S5).
- **A scene the player reads for what happened is a story told by the place; the elements draw from the main premise** (cited, S3).
- **Overheard banter and thinking aloud are the cheapest way to make a place feel lived in, and they can point at a quest** (cited, S7); **a line matched to the world state makes the ambient voice notice what the player did** (cited, S7, Ruskin).
- **Reputation is what a faction knows about you; pleasing one side angers another** (cited, S6).
- **A hub's first act is a long tutorial that teaches by escalating its challenges, always with more than one way through** (cited, S5).
- **An ending composed of per-thread outcomes, seeded early and read late** (cited, S8 §3).

#### Rules this campaign adopts

1. **Each line has a body that is not talk** (authored, from S1), and at most two `talk-to` objectives, the hub and the finale excepted (the design gate's ruling): the castle is a search with one puzzle (get, use), the lighthouse a hide-and-seek (spy, get), the loaf a gathering with a vessel on the mountain (get, use) and a door won one of four ways (exchange, steal, listen, report), the chorus a hunt by ear, bell and name (listen, use), the curtain an investigation (get, listen, report). Talk opens a line and closes it; it is never the body.
2. **Every needed find has three ways to be found** (authored, from S2): its hint, the line's own speaker who names the place again, and the thing itself, which stands out in its place. A clue that unlocks a better answer is never the only answer: the plain answer stays.
3. **The door the loaf needs has four ways** (authored, from S2 and S4): talk Runa round with what a found page tells, trade her what was found on the mountain, lift it off her bench while she is busy at the anvil, or admit what she wants admitted (the n+1 of S5: always open). Runa remembers which, and says so later.
4. **Side content is exploration that pays** (authored, from S3, S7): eight overheard scenes, two of them pointing at a strand; nine finds that each tell a piece of the town's story and pay a penny, five of them opening a better line with someone; a stall that sells for pennies.
5. **The curtain is an investigation** (authored, from S2): three clues, each a thing found in the town, three witnesses in their own dialogue, the answer named in a dialogue choice; the right answer is always on offer and each clue adds a better way of saying it; a wrong name costs a friendship until it is mended (from S6: what one side knows of you).
7. **The castle holds one environmental puzzle** (authored, from S3: the place tells the story): three candles in three rooms, lit in the order the play is told, which the hub names and the candles' colours carry; a candle pressed out of turn will not take, and says so.
6. **No combat, no fail state** (pinned by the owner); a wrong move costs a line of dialogue, never progress.

#### How long, and how it is estimated

Estimated, not measured; the measurement is the owner's next playtest. The method: the previous version's owner playthrough, 18 objectives (16 talks, 2 reaches) and the route the build measured (2380 blocks), took about 20 minutes, so a talk-and-walk objective costs about one minute and the route is walked at about twice the engine's 60 blocks a minute. On that rate, each activity is budgeted from what the player does at it (authored): a talk 1–2 min (the new trees are about twice as long), a find with its search 3–5 min, a use with its vessel 2 min, an overheard scene 0.5 min, a side find with its reading 1–2 min, a shop visit 2 min, plus the new route at 120 blocks a minute. The per-line sums and the total are in `DESIGN.md`, *How long*.

### The design gate

Answered by the planner for the owner: yes, with three changes, applied in the step 3 documents and `DESIGN.md` before step 5. The chorus became the hunt itself (the tub, the bell and the hull are pressed; two talks); every line holds at most two `talk-to` objectives, the hub and the finale excepted; the curtain became the investigation, with a wrong name that costs something and can be mended; the castle search holds one environmental puzzle, the three candles. The approved pictures under `design/` stand: the map did not change, and no picture was drawn.

### Content (steps 5 to 7)

`quests.json` and `dialogue.json` were written from the design; the zh-cn sidecar is transcreated by the configured provider (650 keys, exact coverage). Census of the build that ships: 35 objectives, 12 `talk-to`, 4 `reach-anchor`, 3 `collect`, 16 `interact`; 18 triggers (8 overheard, 9 finds, 1 press on the oven door), 3 pulses, 1 firework, 1 stall of 4 offers; 14 dialogue trees, 69 nodes. `analyze` exits 0 with `DW0467` (the ghast's hum, carried from the previous version), `DW0813` and `DW0822` (3238 blocks of route, about 54 minutes at the table's rate).

What the engine at 1.15.0 refused on the way, and what stands in for it:

- A lectern cannot be a prop (`DW1059`); a conjured chest cannot stand among scenery barrels (`DW1024`); no prop may stand on a way's mark (`DW1057`); a fence prop made a pen (`DW0921`). The finds are signs, pots and the like, on the marks of plots.
- A trigger the critical path needs must be in sight where it becomes pressable (`DW0863`): the candles arm when the party reach the lady's rooms.
- The candle latch was first a party datum with a reset on a wrong press, then three triggers gated on that datum, then three triggers chained by flags. The proof credited the latch flag to one press in the first two forms (the critical path held only the yellow candle) and refused the third as an undeclared fork (`DW0480`). The candles are three ordered `interact` objectives, the compass hidden, each hint naming the play's scene and never the colour; a candle pressed out of turn answers that it will not take. The reset is gone.
- PackTest's prop test asserts every prop at tick 0 in a world it shares with the tests that press or complete the oven door, which cleared it. No effect clears a prop's cell: a found pumpkin is chalked and rolled home by the children; the oven door stays on Runa's bench.
- An ungated completing option that set a flag beside gated siblings that set others had `flag/loaf-done` refused as an undeclared fork; the always-open way sets no flag. The proof took a gated door option first, putting a side find on the path (`DW0863`); the always-open way stands first.

### Build, cameras and detail (steps 8, 8b, 9)

- Step 8's first build refused `DW0430`: the new route crosses the outer tread columns of `node/flight-6` and `node/flight-7` sideways. Each was re-authored by its own agent from its handout (attempt 1, the build's refusal as the finding): the outer columns are masonry and low wall kerbs.
- The castle declares nine of the rooms its program already marks as stations; its `detail --check` passes (688 s, 2.44 GB peak).
- The written-world check later found a dirt path under two props (below); `node/poi-spring` and `node/cottages` were re-authored by their own agents (attempt 2 each): the cell under each mark is cobblestone and packed mud.

| place | attempt | handout | repaired | commit |
|---|---|---|---|---|
| `node/flight-6` | 1 | `.out/handouts/flight-6/handout-1.md` | `DW0430` | written (178 s, 3.18 GB) |
| `node/flight-7` | 1 | `.out/handouts/flight-7/handout-1.md` | `DW0430` | written (613 s, 1.90 GB) |
| `node/poi-spring` | 2 | `.out/handouts/poi-spring/handout-2.md` | `DW0955` | written (638 s, 2.07 GB) |
| `node/cottages` | 2 | `.out/handouts/cottages/handout-2.md` | `DW0955` | written (641 s, 1.91 GB) |

- Step 8b: the six cameras whose subjects changed (street-far, lane-far, forge-near, weaver-near, stage-near, square-near) were drawn again (463 s, 2.6 GB peak); each still frames its picture, and none moved.
- The cottages' letter and the spring's basin stood on a dirt path the server turns to dirt under a block it treats as solid (the written-world check below); the weaver's mark is the drying frame's board, and Elin stands in her loom room (`node-weaver` + `[7, 0, 0]`), off the shop's one walkway, where her body had stalled the bot.

### The machine ladder (step 10), on the build that ships

Manifest `c87b8d3f40a18c4eea607747d653da4da7d925a4eea65b9b9abefb884aaa203d`, content `67187b4f`, built on the Linux x86-64 build machine (14:41 wall, 3.48 GB peak); the same documents built on macOS arm64 at an earlier revision gave the same manifest as the build machine (`285ac653`, then `a24c56b8`).

- PackTest exit 0: 179 of 179 required tests (93 s).
- Bot critical path exit 0: 27 steps PASSED, 4 advisory findings; 14 watchers, 9 within reach on the proven path and asserted; 2 of 3 pulses heard at a listening station (the cooper's hum has no station on the forced route, the chorus being optional); 21:52 wall.
- Written world exit 0, verdict pass: `model` 0 differing cells of 5038534 compared; random-tick 8, re-derived 28740, each the server's.
- Several players at once: five bots in one world, one per line from the hub, started together; every line step of every bot passed and each stopped at its closing campaign check, the finale being no line's step (576 s).
- Branch runs: the build enumerates 160 story worlds, 32 distinct walks (`validation/world-path-*.json` by sha256; the other 128 walk the same bytes, the door's and the wrong name's alternatives being counted but never walked). One world per distinct walk, the lowest-numbered, was run in five tiers: **30 of 32 PASSED**, endings encore 4, curtain call 12, no ending 14. `world/60` and `world/61` FAILED: both servers were shut down by their watchdog at the same minute, with every server of the five reporting 35–44 s behind, while another job on the build machine held its load average above 80; neither failure is a step of the campaign.

| sha256 (12) | worlds | run |
|---|---|---|
| 01e8256415ad | 0,4,5,9,10,14,15,19 | 0 |
| 4a37cf0ff898 | 1,6,11,16 | 1 |
| 919e16925187 | 2,7,12,17 | 2 |
| 080dbd3a2317 | 3,8,13,18 | 3 |
| a003cc17076d | 20,24,25,29,30,34,35,39 | 20 |
| de7bd4adc953 | 21,26,31,36 | 21 |
| ef39a56e82bf | 22,27,32,37 | 22 |
| 37cb6654a591 | 23,28,33,38 | 23 |
| 66049e5c752d | 40,44,45,49,50,54,55,59 | 40 |
| 3a640aaa4de6 | 41,46,51,56 | 41 |
| 6cbf88f9e8fb | 42,47,52,57 | 42 |
| a77d734897c6 | 43,48,53,58 | 43 |
| 9761bdc8d966 | 60,64,65,69,70,74,75,79 | 60 |
| 3c46e2720e28 | 61,66,71,76 | 61 |
| 7adb2e22c2c9 | 62,67,72,77 | 62 |
| df56b7977c1a | 63,68,73,78 | 63 |
| d5ed91dc8a49 | 80,84,85,89,90,94,95,99 | 80 |
| f46515e8cf5a | 81,86,91,96 | 81 |
| e69bc7a72fe4 | 82,87,92,97 | 82 |
| b00b6ec72f89 | 83,88,93,98 | 83 |
| f8176853105f | 100,104,105,109,110,114,115,119 | 100 |
| 93113056a452 | 101,106,111,116 | 101 |
| bdde4232e142 | 102,107,112,117 | 102 |
| b6d8ac2136f2 | 103,108,113,118 | 103 |
| 9969319e398e | 120,124,125,129,130,134,135,139 | 120 |
| f44be64776d4 | 121,126,131,136 | 121 |
| eebaf6bb19eb | 122,127,132,137 | 122 |
| 21e2a84eaa7c | 123,128,133,138 | 123 |
| 2b3450df408b | 140,144,145,149,150,154,155,159 | 140 |
| c5548134265c | 141,146,151,156 | 141 |
| 108bdc5a3cff | 142,147,152,157 | 142 |
| 0b8aabdb8c17 | 143,148,153,158 | 143 |

(The map is of the build at `1b07da3c`; the walks are the same set on `c87b8d3f`, whose change moved one body.)

### Branch chronicle (step 11)

All 160 chronicles of the build that ships were read against the flags each world holds: every fork choice appears in exactly the worlds holding its flag (the tail, the Founder and the Loaf: 80 present, 80 absent each; the chorus and the curtain: 96 and 64), none missing and none stray; the ending each world reaches follows its Loaf (no ending on the forge in all 80, the oven's two endings split by applause: encore 32, curtain call 48).

### Visual review (step 12)

`delvec frames` on the build at `a24c56b8`: `renderer: lumenwright 0.3.0, backend apple m2 pro (metal) (auto)`; 1623 shots (1271 POV, 198 interior, 123 threshold, 16 interact, 14 NPC, 1 spawn), 366 s, 3.9 GB peak. Every new pressable reads as what its text names (the candles, the pumpkins, the recipe board, the hive, the tub, the bell, the boards, the lever); the hive's frame stands its camera inside the block. The route still crosses the open hillside between the town and the castle (the router, recorded in round 1).

### Hand-over (step 13)

The staging gate on manifest `c87b8d3f`, with the bot's run report and the written-world record: **STAGEABLE**, admitted with no override; 63 of 159 finding classes inapplicable. On the way, the gate refused the three `collect`s that conjured a chest (findings `isl-33`, `isl-53`, unbound); those finds are chests the party opens. The storybook's "what kind of delve" section is rewritten for searching, the bit of puzzling, the finds that pay a penny and the stall; the zh-cn edition's changed paragraphs are transcreated by the provider. Nothing is staged by this run.
