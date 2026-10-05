# The Floor That Was a Lid

The demo level for **a killing volume live from a story stage** (spec-0088):
`when` on a `lethal_volumes[]` entry, the volume held per quest
configuration, and the danger-is-visible check judged in every configuration a
body can meet it in — including the last one before it goes live.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-floor-that-was-a-lid/

Its one piece, `prefab/lid-room`, is in the prefab library
(`prefabs/lid-room.{nbt,json}`) and is expanded from the grammar program
`campaigns/the-floor-that-was-a-lid/design/programs/lid-room.json`
(11 × 8 × 17, seed 1, named in `zones.json` beside it).

## What it is

One stone-brick hall, open to the noon sky, floored in polished andesite. You
arrive at its north end (5, 68, 2), facing south. A lever hangs on the far
(south) wall.

- **The lid.** The middle of the floor — a 3 × 3 patch around (5, 67, 8) — is
  the roof of a pit. It is the same andesite as the rest of the floor; nothing
  says it is different.
- **The pit.** Two courses of air under the lid, lit by four glowstone blocks
  set in its walls, with a polished blackstone bottom. Its bottom course is the
  killing volume `lethal/the-pit`, staged on `flag/lid-fell`: dead until the
  lever is pulled, live from then on.
- **The lever** (5, 69, 15). Pulling it sets `flag/lid-fell` and clears the
  lid in the same beat, so the floor that was a lid becomes a hole in the same
  tick the pit's bottom starts to kill.

## What to look for

1. **At the spawn**, look down the hall: one plain floor, one lever at the far
   end. Nothing marks the middle.
2. **Walk straight down the middle to the lever.** You cross the lid. Nothing
   happens: the volume under you is not live, and the floor is floor.
3. **Pull the lever.** *Behind you, the floor falls in.* Turn round: the middle
   of the hall is a 3 × 3 hole.
4. **Walk back to the hole and look down** (the objective completes at the rim,
   (5, 68, 6)). You see the lit pit and its black floor three courses down —
   the danger is in plain sight now, where before the beat it was under your
   feet and safe.
5. **Step in.** You die at the bottom, the pit's own line is shown (*The floor
   was a lid, and the pit under it has no bottom you would survive.*) and
   *The pit keeps what falls into it. You wake where you came in.* You respawn
   at the north end.
6. **Walk out**: back to the spawn. The delve completes.

## The compile transcript, beside the walk

```
danger-visibility binding: 1 volume(s), 1 staged; judged over 2 configuration(s) as 2 (volume, configuration) pair(s) against walked populations of 126..135 cell(s); 0 caught, 0 shown, 0 read as safe floor; 0 declaration(s) of 0 borne out by the bytes; 1 of 1 volume(s) reached by a body the engine models (in 1 of 2 pairs).
```

One volume, judged in two configurations: the one before the lever (the
volume dead, the pit roofed — no body can reach it) and the one after it (the
volume live, the hole open — reached by a fall). `validation/lethal-gate.json`
carries both rows: `reached_by` null before, *a player, by a fall* after.

## The refusals

The same campaign with one edit each, built with the same engine. Verbatim.

**The volume raised to the floor course** — `region` moved onto `anchor/lid`
with `extent [1, 1, 1]`, so it reaches the floor a body stands on over the
lid. Refused in the configuration before the lever, because a body standing
there when the gate flips has no tick in which to step off:

```
DW0891 [error] build: lethal volume `lethal/the-pit` goes live at step 2 of the critical path and a body may be standing on these cells when it does; nothing in the world before that beat says they kill: y=68 (25 cell(s): [3, 68, 6], [3, 68, 7], [3, 68, 8], [3, 68, 9], [3, 68, 10], [4, 68, 6], and 19 more on the same floor) (25 cell(s), the configuration arriving at critical step 0, before its gate — requires `flag/lid-fell` — holds). A body standing in a volume's keep-out when its gate flips is killed in the same server tick, with no tick in which to step off, so the floor it stood on must read as danger BEFORE the beat. It declares no `shown_by` at all. Roof or wall the volume's cells off until the beat that opens them (the beat that arms the volume is usually the beat that should open the way to it); lower the volume so its keep-out's top course lies under the floor a body stands on before the flip; or author one of the blocks vanilla hurts a body with under those cells, visible before the flip, and declare it in `shown_by`. Do not declare the floor a place nobody walks, and do not fire the flag later to pass — a hazard that arrives silently under a body is the finding, wherever on the path it arrives.
```

**A way onward through a volume that has woken** (`DW0510`). On this level the
hole is three cells wide in a hall nine wide, so a leg after the beat walks
round it and there is nothing to refuse; the shape is shown on the engine's own
lid-room fixture (`crates/delvec/tests/staged_lethal.rs`), whose waist volume
spans its hall and is armed before the leg to the exit:

```
DW0510 [error] build: critical path: the only route from [12, 68, 6] (floor [12, 68, 6]) to [2, 68, 2] (floor [2, 68, 2]) runs THROUGH lethal volume(s) `lethal/the-waist` — the party cannot reach this objective without dying on the way. The geometry is walkable; the volume is what closes it. In this configuration: `lethal/the-waist` is live from a story stage (requires `flag/lid-fell`) and is live in the configuration arriving at critical step 2. Move or shrink the volume, give the party a route around it, or — for a volume live from a story stage — move the beat that arms it after this leg; do NOT delete the volume to silence the proof.
```

**The volume staged on a datum one player holds** — `when` reading
`state/nerve`, declared `player`-scoped. Refused at the document, with no
world built:

```
DW0953 [error] quests /content/lethal_volumes/0/when/requires_state/0: lethal volume `lethal/the-pit` is staged on `state/nerve`, which is `player`-scoped — a volume's liveness is a fact about the place, so a term one player satisfies and another does not would be a pit that kills one body and spares the one beside it, and the sweep's entity half has no player to read a per-player score from. Name a flag or a `party`-scoped datum in `when`, or leave `when` out to make the volume live from world-load
```

## Serve it locally

From the engine repository at the branch that carries spec-0088
(`feat/staged-lethal`), with this content repository's worktree as the
library:

```
tools/creator/playtest-server.sh up <content>/campaigns/the-floor-that-was-a-lid --prefabs <content>/prefabs
```

then Multiplayer → Direct Connect `localhost:25565`, pick **Visitor**, and walk
the steps above. `tools/creator/playtest-server.sh down` when done. The level
is never copied into a singleplayer save.

## State

Built and machine-proven with the engine at `feat/staged-lethal`: two builds
byte-identical; PackTest 19 of 19, among them `lethal_the_pit` (gate open, the
dummy in the box dies) and `lethal_the_pit_shut` (gate shut by one term, the
dummy lives) — each red alone under its own strip (the tick's guard removed:
`lethal_the_pit_shut` fails, *expected 20, got 0*; the entity sweep removed:
`lethal_the_pit` fails, *expected ..0, got 2000*). The mineflayer critical
path passes in 5 steps; before each walk it asks the server whether the pit is
live (`lethal/the-pit shut` before the lever, `live` after it), and its
death loop enters the pit, dies there, reads the pit's own line and reports
`staged_live_at_trial` 1 of 1.

The staging gate refuses this build: 2 of 122 findings have no live, binding
check on it — `drill3-01` and `drill3-03` (it carries no design record).
Not yet walked by a person.
