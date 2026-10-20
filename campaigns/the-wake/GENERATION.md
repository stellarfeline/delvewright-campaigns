# The Wake — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0014 (actors, staging, cutscenes)
pinned: a funeral procession level that is mostly staging — mourners walk, a
eulogy sequence plays, one player choice redirects the procession. Small, one
mechanic family, minimum cast. Languages: English, and zh-CN transcreated.

## Where the story came from

The level was built once before, on a pre-site-plan engine at dsl 0.8.0
(content branch `campaign/the-wake`), from a pool prefab that no longer exists
in the shape this engine builds. Its design record held the premise, the cast,
the five quests, the branch table and the dialogue. Those were transcribed, not
re-authored, and moved onto dsl 0.55.0; what changed is listed below.

- The map is new: a site plan of two places (the beach and the barrow field)
  joined by open ground, detailed from the campaign's own programs written by
  `design/build_pieces.py`, instead of one 48 × 40 library piece.
- Anchors are renamed for what they are (`anchor/bier`, `anchor/warden-post`,
  `anchor/tide-line`, …) instead of the library piece's generic names.
- The three mourners carry names (Maud Pell, Old Garrow, Tam) and the
  lamp-bearer is Orrin: three bodies named "Mourner" are one name on several
  declarations.
- The warden's barrel of loot is gone: it was not part of the mechanic.
- The two dialogue edges the earlier build needed as flow plumbing are gone:
  this engine's flow model reaches the cast ledger's later roots, so Sedge's
  rite and Hallis's word are served by the ledger's dialogue swap alone.
- The narration that answered the choice moved into Hallis's reply: a dialogue
  option sets no `narrate`, and a quest-level `narrate` takes no flag gate, so
  each answer goes on (`next`) to the node in which he answers it.
- Compass words left the player-facing lines (`DW1049`): "south past the fire"
  became "past the fire", and every hint names a landmark.
- `obj/bring-the-word` is titled "Answer the brother" (`DW1045`): the
  completion is a talk.
- The art titles stay ASCII in the zh-CN sidecar (`DW0328`): the art font has
  no Han glyphs.

## What was invented here

- The islet under the foot of the keep wall, the tide stones along the
  waterline that keep a body out of the sea, the dykes down both sides, the
  shut timber gate in a dressed arch.
- The faces of Sedge and Hallis (`skins/cast.json`, composed by `delve_skin`).
- The bier dressed in a brown leather shroud.

## Posture note

The rite is told flatly and the grief is not explained. Hallis says outright
that he cannot choose and why; Sedge never softens a fact. Neither ending says
which answer was right: each says what became of her, and stops.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level; its approved design is its queue row,
and `world.json` declares `demo_level: true`. `design/` holds only the program
generator; `design.json` does not exist and no showcase camera is written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.55.0, mc 1.21.11` from the engine's `main` at
`63be47f82ed89b4bf52c6393684f742bb926b7f0`, an unreleased tree. Its version
string is the same number as the released `delvec--v1.13.0`, which answers a
different dsl number, so the revision is what names the engine. The skill has
no way to name an unreleased engine revision as a campaign's pin, so no pin was
written; this paragraph is the record.

No shipped library taken: both pieces are this campaign's own programs under
`programs/` at program version `1.9.0`, frozen by `delvec detail` into
`prefabs/the-wake-*`.

## The skill run

Authored through `/new-delve` as the engine tree above carries it, not through
an installed plugin, with that tree's own `target/release/delvec`
(`cargo build --release -p delvec`, exit 0) through an environment file of the
run's own. Init's pin check (I1b) refuses that arrangement (exit 3): it reads
the machine's shared `~/.delvewright/env.sh`, which names the released engine,
and offers no way to name this tree without rewriting it.

## Target length

`target_minutes` is 15. The critical path measures 48 blocks of route over the
graph (28 over the built blockout's legs); the rest of the level is the staging
itself — the wake filling the field, the rite, three cutscenes — and reading.

## The branch chronicle

Read from `world-chronicle-0.md` (`branch/ground`, flag/to-the-ground set) and
`world-chronicle-1.md` (`branch/tide`, flag/to-the-tide set) of the build at
manifest `3c1f4eb803c6d6bbbb5896f5544c6491da49d094cfd149e0056bca7b06ab981b`,
each end to end, against `DESIGN.md` and against the dialogue reachable in that
world. Lines 1–15 (the landing, the wake assembling, the rite, the walks of
Orrin, Tam and Sedge, the word asked) are the same in both; the worlds part at
line 16, the choice.

| claim reviewed | world(s) | chronicle line(s) | verdict |
|---|---|---|---|
| design: the wake assembles behind the party as the bell tolls | 0, 1 | 3–7 `arrives` ×5 | cleared |
| design: Orrin, Tam and Sedge walk during the rite | 0, 1 | 11–13 `arrives` | cleared |
| Sedge: "Ground, then. The cut is at the end of the row, where I was standing when you came up." | 0 | 13 `arrives` (Sedge left her post), 16 `believes` the ground | cleared |
| Sedge: "Water, then. I do not walk to the water. The cut stays open tonight…" | 1 | 16 `believes` the water; no `seals` on the cut | cleared |
| Hallis: "You said the ground… watch you carry her along the row." | 0 | 16 `believes` the ground | cleared |
| Hallis: "You said the water… until the ebb has her." | 1 | 16 `believes` the water | cleared |
| Narration: "The plank goes down. From the head of the row Sedge says the last of it…" | 0 | 13 (Sedge at the row's head), 19 `arrives` at the cut | cleared |
| Narration: "The row is one longer. By morning the field will be level again, and it will keep her." | 0 | 20 `departs`, 21 `seals` the cut | cleared |
| Narration: "They wade her out to the line and let go…" | 1 | 19 `arrives` at the tide line | cleared |
| Narration: "She goes out on the ebb, the way she went out every morning of her life." | 1 | 20 `departs`, 21 `loses` | cleared |
| design: only the bier crosses the fork, one walk per branch | 0, 1 | 19 `arrives` (world 0 the cut, world 1 the tide line) | cleared |

## Machine ladder

On the build whose manifest sha256 is
`3c1f4eb803c6d6bbbb5896f5544c6491da49d094cfd149e0056bca7b06ab981b`, engine
`63be47f82ed89b4bf52c6393684f742bb926b7f0` force-rebuilt on the remote Linux
machine (`cargo build --release -p delvec`, exit 0): two builds there
byte-identical, and a third on macOS with the same manifest. The ladder is
**green**.

- **PackTest: 54 of 54 required tests pass.**
- **Critical-path bot: green.** `critical path 'the-wake' PASSED (7 steps, 4
  advisory finding(s))` — the four are the absent death plan, crush gate and
  combat plan, and the branches the critical-path run does not drive.
  `[watch] 2 watcher(s) in the record, 2 within reach on the proven path, 2
  asserted (18 judgement(s))`; `cue binding: 6 of 6 owed cue(s) arrived at the
  bot`. Die-retry is unbound: no combat, no death plan.
- **Branch runs: 2 of 2 worlds pass**, each in its own fresh world: world 0
  (the ground) and world 1 (the tide), each `PASSED (7 steps)`.
- **Written world (`DW0955`): green.** 800 cells compared, 0 differing in the
  model class and 0 in the clock class; 4 differ in the named server
  re-derivation class (four headstones beside the mounds drawn with a `low`
  side where the model writes `none`). 0 item entities.
- **Staging gate: admits** the build on those two records: all 139 findings
  carry a live, binding check or a justified exemption; 55 of them are
  inapplicable, this campaign declaring none of their objects. The gate reads
  the level as a declared demo level named by its queue row.

## Visual review — deferred

The Chunky render set (27 scenes) was not rendered; it waits for the
Lumenwright review frames. The layout was judged on CPU drafts
(`delvec snapshot`): the spawn shot, `pov/leg1/wp0` (up the grave road at the
keep gate), `pov/leg2/wp2` (arriving at the warden's post) and an overview from
over the sea. They show the beach, the field, the grave road, the graves on
both flanks and the keep wall with its gate. The draft renderer draws a
lantern on a fence post as a solid block, so the lamps are not judged there.
No storybook image is shipped for the same reason.

## Toolchain friction, by where it bit

- Init I1b: no way to name an unreleased engine revision; the pin check
  refuses (exit 3) a run on this tree.
- Step 2: a one-place map cannot be detailed. The piece gate requires the entry
  space to carry an exterior traversal edge (`contract-well-formed`), and the
  detail binding refuses that edge as a way out no seam allocated (`DW0844`);
  the beach became a place of its own so each piece has a seam to answer.
- Step 5: the bier's walks sit in branch quests gated by their objectives, but
  the actor-walk planner reads a branch only from the walk effect's own `when`.
  Without one, the tide walk was planned from the ground branch's destination
  and started five blocks from the bier, with no diagnostic. Each walk now
  declares its branch in `when`.
- Step 5: a `narrate` takes no flag gate and a dialogue option takes no
  `narrate`, so a line answering a choice lives in the NPC's reply node.
- Step 10: `branch-runs.sh` run under the bot's project removes the bot's
  `run-report.json`, which the staging gate requires; the bot was re-run under
  a project of its own (`dw-the-wake-r1-bot`), green, on the same manifest.
- Localization: `i18n-translate.py` reads its config from the engine tree
  (`--config` used instead); it wrote the art titles in Han, which the art font
  cannot draw (`DW0328`), and they were set back to the English by hand.
