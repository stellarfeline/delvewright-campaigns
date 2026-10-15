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
`d500e8761f1c03507166c2ddcde61b5c9bf75af8` — an unreleased tree, the only one
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

## Known engine issue, not worked around

Quest UI sounds — the new-objective cue, the objective-complete orb, the
campaign-complete toast — play at the world spawn rather than at the player.
A fix is in flight on the engine's main line.

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
end, against `DESIGN.md` and the dialogue reachable in that world. The
callbell is an ambient trigger and no field of a trigger's effects carries a
`happening`, so no chronicle line records it; its claims are licensed by the
chronicle's own `Flag assignment` header (`flag/bell-rung=set|unset`) and the
plan's `entry_deeds`, and that gap is recorded as toolchain friction.

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
