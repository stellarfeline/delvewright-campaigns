# The Reckoning — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0108 pinned: a three-room shrine
with three threads — a bell to strike, a prisoner to free or leave, a ledger
to burn or keep; a finale whose keeper speaks the outcome of each thread;
three endings chosen by the tally and the deeds; an aftermath per ending (the
shrine floods, the shrine stands, the shrine burns) that the party stands in
when the camera returns. Every gate of the final scene is an input whose
writers are judged (`DW1029`, `DW1030`); the aftermath is proven by a PackTest
per (ending, world) and read by the bot. Small, one mechanic, minimum cast.
Languages: English, and zh-CN transcreated.

## What was invented here

- The fiction: Wend Mere, drained once a year; the Tallyhouse in its bed; its
  keeper Ysolde Marrow; Tobin Reave held in the cell against his family's
  grain debt; the callbell that calls the valley down to the mud.
- Which act is which kind of writer, so that every kind the spec counts is
  present: the bell is an ambient `use` trigger (a deed, *did*), the cell is a
  dialogue choice (*said*), the ledger is an optional quest (a deed,
  *finished*).
- The tally, `state/tally`: the people the party answered for — the valley
  (bell) and Tobin (freed). The ledger is the deed that overrides it.
- The three endings: burned ledger → the house burns; otherwise tally ≥ 1 →
  the house stands; tally 0 → the house floods.
- That a finished house holds nobody: in the burning and the flooding,
  Ysolde lets a still-chained Tobin out herself.
- The keeper's per-thread speech is a dialogue chain, one node per thread,
  each node chosen by that thread's flag, so the player reads it at their own
  pace; her verdict and one epilogue line per thread are narrations in the
  final scene.

## Engine and language

Built with `delvec 1.13.0, dsl 0.46.0, mc 1.21.11` from the engine's
`feature/endings-read-the-run` at
`d0e482b80d1c75e86ee2c5607d0fac4554de3713` — an unreleased tree, the only one
carrying spec-0108. Its version string is the same number as the released
`delvec--v1.13.0` (which answers `dsl 0.39.0`), so the version alone does not
say which engine built this level; the revision does. The skill has no way to
name an unreleased engine revision as a campaign's pin (the content
repository's `versions.toml` pins one release for every campaign), so no pin
was written; this paragraph is the record.

No shipped library taken: every piece is this campaign's own grammar program
under `programs/`, frozen by `delvec detail` into `prefabs/the-reckoning-*`.
The two faces are composed from `skins/cast.json`.

## Posture note

Three axes pushed off the default: (1) people name their feelings outright —
Tobin says he is frightened and why, Ysolde says she no longer knows whether
the house does any good; (2) the keeper's judgement is the story's, and it is
not softened — doing nothing for anyone floods the house, burning the debts
burns it; (3) the endings do not explain which was right: each says what
became of the house and of each thread, and stops.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Target length

`target_minutes` is 10. The critical path measures 42 blocks of route over six
legs (about a minute of walking); the rest is reading — Ysolde's summons,
Tobin's plea, the reckoning — and the two elective acts.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), not
through an installed plugin, with that tree's own `target/release/delvec`
(`cargo build --release -p delvec`, exit 0) through an environment file of the
run's own. Init's pin check (I1b) refuses that arrangement (exit 3): it reads
the machine's shared `~/.delvewright/env.sh`, which names the released engine,
and offers no way to name this tree without rewriting it.

## The reading, as built

`ending binding: 3 ending(s); 15 input(s) read, 15 seeded (9 with a deed
among their writers), 0 final-scene only; 8 story world(s) enumerated (56
unrealizable target(s), 0 at the bound); 18 aftermath effect(s), 18 of them
observable after the scene.` Each ending reads five inputs —
`flag/bell-rung` (did, ambient), `flag/ledger-burned` (finished,
`quest/the-ledger`), `flag/tobin-freed` and `flag/tobin-left` (said,
`quest/the-cell`), `state/tally` (did and said) — all seeded; the declaration
`endings_read: {at_least: 3, deeds_at_least: 2}` holds for each with 5 seeded
and 3 with a deed. `DW1029` and `DW1030` are silent: every ending is reached by
a story world (burns by worlds 0, 2, 4, 6; stands by 1, 3, 7; floods by 5).
Eight `ending_<slug>_<k>` PackTest templates are emitted, one per (ending,
witness world), asserting 1–3 observables each.

## The branch chronicle

Read from the eight `world-chronicle-<k>.md` of the build at manifest
`aae55980e460a8188cbd6e32f9377a161162e1cbcd3cc7583b4521da7d35a50b`, each end to
end, against `DESIGN.md` and the dialogue reachable in that world; the build at
manifest `0a6cbe0d8efa9ef7feea82f2656c0beb9ffb08f260bff49bfd3beae6f8f5d9d1`
writes the same eight chronicles byte for byte. The callbell is an ambient
trigger whose `set-flag` declares no `happening`, so no chronicle line records
it; its claims are licensed by the chronicle's own `Flag assignment` header
(`flag/bell-rung=set|unset`) and the plan's `entry_deeds`.

| claim reviewed | world(s) | chronicle line(s) | verdict |
|---|---|---|---|
| Ysolde: "You rang the callbell. The valley came down onto the mud…" | 0, 3, 4, 7 | header `flag/bell-rung=set` (no line: ambient trigger) | cleared |
| Ysolde: "Nobody rang the callbell. The valley stayed at home…" | 1, 2, 5, 6 | header `flag/bell-rung=unset` | cleared |
| Ysolde: "You let Tobin Reave go. He is halfway home by now…" | 0, 1, 2, 3 | 5 `gains`, 6 `survives` (the walk out), 7 `departs` | cleared |
| Ysolde: "Tobin Reave is still chained in his cell. You heard him out, and you left him there." | 4, 5, 6, 7 | 5 `survives` (left chained); no `departs` before the scene | cleared |
| Ysolde: "And the ledger is ash in the brazier…" | 0, 2, 4, 6 | 9 (worlds 0, 2) / 7 (worlds 4, 6) `loses` `obj/burn-the-ledger` | cleared |
| Ysolde: "The ledger is still on its stand…" | 1, 3, 5, 7 | no `obj/burn-the-ledger` line; header `flag/ledger-burned=unset` | cleared |
| Narration on freeing: "Tobin is past you and out through the porch…" | 0, 1, 2, 3 | 6 `survives`, 7 `departs` | cleared |
| Verdict: "There is nothing left for this house to keep… Out, all of you." | 0, 2, 4, 6 | 12 (0, 2) / 11 (4, 6) `loses` — the house burns | cleared |
| Verdict: "This house did some good this year. It can stand another." | 1, 3, 7 | 10 (1, 3) / 8 (7) `survives` — the house stands | cleared |
| Verdict: "…I am opening the sluice… The mere can have it." | 5 | 9 `loses` — the house floods | cleared |
| Epilogue: "Tobin Reave is home before dark. You let him go." | 0, 1, 2, 3 | 7 `departs` | cleared |
| Epilogue: "Tobin Reave stays chained in the cell, held for next year's reckoning." | 7 | 5 `survives`; no `departs` | cleared |
| Epilogue: "Ysolde pulled Tobin's pin herself on her way past the cell…" | 5 | 8 `departs` (`then/10`) | cleared |
| Epilogue: "Ysolde pulled Tobin's pin herself on her way out. She would not burn a man with her house." | 4, 6 | 10 `departs` (`then/11`) | cleared |
| Epilogue: "The callbell brought the valley down onto the mud…" / "Nobody heard a bell…" | 0, 3, 4, 7 / 1, 2, 5, 6 | header `flag/bell-rung` | cleared |
| Tobin's barks in the finale ("Is it over?…", "You could still pull the pin…") | 4, 5, 6, 7 | 5 `survives`; the cast places him only on `flag/tobin-left` | cleared |

## Machine ladder

On the build whose manifest sha256 is
`0a6cbe0d8efa9ef7feea82f2656c0beb9ffb08f260bff49bfd3beae6f8f5d9d1` (two
builds byte-identical on the remote Linux machine; a third, on macOS, has the
same manifest), engine `d0e482b80d1c75e86ee2c5607d0fac4554de3713`, with no
campaign change from the previous ladder. The ladder is **green**.

- **PackTest: 44 of 44 required tests pass**, all eight
  `ending_<slug>_<k>` templates among them (burns 0/2/4/6, stands 1/3/7,
  floods 5), `v04_move` and `watch_yield_npc_tobin` among them. Tobin's walk
  takes his body away on arrival (`on_arrive`: `despawn-npc`), so the template
  reads the walk on the tick before the arrival, with the body present and its
  watch still yielded.
- **Critical-path bot: green.** `critical path 'the-reckoning' PASSED (5
  steps)`; the aftermath it asserts is the stands' candles alone. `cue binding:
  4 of 4 owed cue(s) arrived at the bot (3 announced objective(s) in the
  build), 3 of the 4 judged farther than 16 blocks from the world spawn; 3 of 3
  other cue packet(s) at the bot`. `[watch] 2 watcher(s) in the record, 2
  within reach on the proven path, 2 asserted (22 judgement(s))`.
- **Branch runs: 8 of 8 worlds pass, and every ending is reached**, in one run
  of all eight: worlds 0, 2, 4, 6 (the house burns), 1, 3, 7 (the house
  stands) and 5 (the house floods), 0 mocked in each.
- **Written world: green.** `world-save.sh`, `delvec written-world`,
  `check-written-world.py --record`: 1031 non-air cells written, 1031 in the
  server save, 1031 compared, 0 differing in every class, 0 item entities.
- **Staging gate: admits** the macOS build on these two proofs: all 129
  findings carry a live, binding check or a justified exemption; 58 of them
  are inapplicable, this campaign declaring none of their objects.

## Visual review — deferred

One frame was rendered and checked: `pov/leg0/wp0` (arriving on the mud,
facing the shrine door), on the build at manifest `aae55980…`. It read as a
flat brick face with a hole in it and a mud floor tiled by clay patches; the
porch front was rebuilt (door frame, lintel, windows, band, corners) and the
clay taken out, checked only on a CPU draft (`delvec snapshot`). Not rendered:
the other 36 scenes of the set, among them every interior, both NPC shots, the
ledger's interact shot, the panorama and the arrival frames at Ysolde and at
Tobin (two of those were in progress and were stopped). The rest waits for the
Lumenwright review frames. No storybook image is shipped for the same reason.

## Toolchain friction, by where it bit

- Init I1b: no way to name an unreleased engine revision; the pin check refuses
  (exit 3) a run on this tree. The content repository's pin is one release for
  every campaign, so the campaign carries no pin.
- Step 5, `DW0204`: a dialogue option gated on `requires_state` over a datum the
  mainline cannot date is "not reachable", so the keeper's verdict moved out of
  dialogue into the scene's narrations.
- Step 5, `DW0542`: a teleport gated on `flag/ledger-burned` was refused for
  covering the brazier's interact hitbox, which that flag implies is already
  gone; the sanctum was re-lined so no one stands outside the volume.
- Step 5, `DW0862`: the remedy assumes a beat must be announced; an elective the
  keeper offers in dialogue is deliberately unannounced, so its hint was removed.
- Step 9: the palette allowlist admits `minecraft:white_candle` (the `_candle`
  suffix) but not `minecraft:candle`.
- Localization: `i18n-translate.py` reads its config from the engine tree
  (`--config` used instead); its fact check passed `伊索德` beside `伊索尔德`
  and three renderings of the keeper, fixed by hand through `l10n-apply`.
