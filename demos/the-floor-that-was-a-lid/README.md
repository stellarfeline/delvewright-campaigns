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
(11 × 14 × 17, seed 1, named in `zones.json` beside it).

## What it is

One stone-brick hall, open to the noon sky, floored in polished andesite. You
arrive at its north end (5, 74, 2), facing south. A lever hangs on the far
(south) wall.

- **The lid.** The middle of the floor — a 3 × 3 patch around (5, 73, 8) — is
  the roof of a pit: spruce boards laid in a stone-brick kerb, a cover over
  something, and floor you can walk on until the lever.
- **The pit.** A plain stone shaft under the lid whose whole floor is a bed of
  nine upward stalagmite points (pointed dripstone tips on dripstone blocks,
  y=65), about eight blocks below the rim. The shaft's walls are unbroken
  stone to the bottom: no opening, no lamp, no floor you could stand on and
  walk away from. Four glow lichen on its walls, just above the points, are
  the pit's only light of its own; after the beat, daylight falls straight
  down the open shaft onto the points. The course just above the points
  (y=66), the one a body that lands on them stands in, is the killing volume
  `lethal/the-pit`, staged on `flag/lid-fell`: dead until the lever is pulled,
  live from then on.
- **The points are the signal; the volume is the mechanism.** Landing on a
  point adds fall damage, and the pit is exactly as deep as it can be without
  the points killing on their own (measured below): a body that steps in
  takes 15 of its 20 health from the points and one that jumps in takes 18.
  The volume kills it on the next tick and shows the pit's own line.
- **The lever** (5, 75, 15). Pulling it sets `flag/lid-fell` and clears the
  lid in the same beat, so the floor that was a lid becomes a hole in the same
  tick the pit's bottom starts to kill.

## What to look for

1. **At the spawn**, look down the hall: one plain floor with a boarded lid in
   its middle, one lever at the far end.
2. **Walk straight down the middle to the lever.** You cross the lid. Nothing
   happens: the volume under you is not live, and the boards are floor.
3. **Pull the lever.** *Behind you, the floor falls in.* Turn round: the middle
   of the hall is a 3 × 3 hole.
4. **Walk back to the hole and look down** (the objective completes at the rim,
   (5, 74, 6)). You see a plain stone shaft and, at its bottom, a bed of
   stalagmite points filling it wall to wall. Ask whether it reads as a drop
   that kills, and whether anything down there reads as a way on.
5. **Step in.** You land on the points, die, and the pit's own line is shown
   (*The floor was a lid, and the pit under it has no bottom you would
   survive.*) with *The pit keeps what falls into it. You wake where you came
   in.* You respawn at the north end.
6. **Walk out**: back to the spawn. The delve completes.

## Why the pit looks like this

A fatal drop has to read differently from a drop you survive or one that leads
somewhere. Each rule below says whether it is cited or authored.

- **Cited.** Pointed and spiked shapes read as deadly and hazardous: "teeth,
  needles, stabbing instruments" (David Orosz, *Shaping Emotions: Utilizing
  Shape Language and Symbols in Level Design*, Game Developer). So the pit's
  floor is points.
- **Cited.** A spike-covered floor is the common alternative to a bottomless
  pit and carries the same message, certain death (All The Tropes, *Spikes of
  Doom*). This pit has a bottom you can see, so the bottom itself carries the
  message.
- **Cited.** Where lethal pits are marked at all, they are marked as unlike
  pits that lead somewhere: *Super Mario Bros. Wonder* gives lethal pits a
  darkened gradient across the bottom, while in *Super Paper Mario* some pits
  drop the player into a secret room instead of killing them (Super Mario Wiki,
  *Pit*). So nothing at the bottom of this pit looks like the floor of a room.
- **Cited.** Lighting draws attention to exits and points of interest and
  guides players through a level (Tom Pugh, *Level Design Tips and Tricks*,
  Game Developer). A lamp-lit floor at the bottom of a shaft therefore reads
  as a destination, so the lamps are gone.
- **Authored.** The pit's own light is glow lichen, which grows in vanilla
  dripstone caves, set on the walls rather than in them: four plants, enough
  for the engine's darkness check (`DW0210`), which refused the cells above
  the points at light 0 with no light in the pit at all.
  The walls stay unbroken stone to the bottom, so no opening suggests a
  passage.
- **Authored, from measurement.** The points never kill by themselves. The
  volume is what the engine counts on, and a body killed by the points before
  the volume acts never sees the volume's line. That fixes the depth (below).

## What the points do to a body

Measured on the pinned 1.21.11 server: a probe server booted from this
campaign's build, pigs given 100 health dropped onto a pointed-dripstone tip
and onto stone, and their health read back.

| Drop | Lands on | Damage |
| --- | --- | --- |
| 13 blocks (the old 78 rim) | stone | 10 |
| 12.3125 blocks (old 78 rim) | a tip | 23 |
| 13.5647 blocks (a jump from the old 78 rim) | a tip | 26 |
| 8.3125 blocks (step off this rim, y=74) | a tip | 15 |
| 9.5647 blocks (jump from this rim) | a tip | 18 |
| 10.5647 blocks (jump from a rim at y=75) | a tip | 20 |

A pig given 20 health, a player's, dropped from this rim's jump height is left
with 2; dropped from the jump height of a rim one course higher it dies.
A tip deals the fall at twice its distance, less 2, rounded up: lethal for a
20-health body from about 10.5 blocks. At the pit's old depth the points would
have killed before the volume acted, so the hall now stands four courses lower,
the deepest rim at which a jump onto the points still leaves the body alive.

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
DW0891 [error] build: lethal volume `lethal/the-pit` goes live at step 2 of the critical path and a body may be standing on these cells when it does; nothing in the world before that beat says they kill: y=74 (25 cell(s): [3, 74, 6], [3, 74, 7], [3, 74, 8], [3, 74, 9], [3, 74, 10], [4, 74, 6], and 19 more on the same floor) (25 cell(s), the configuration arriving at critical step 0, before its gate — requires `flag/lid-fell` — holds). A body standing in a volume's keep-out when its gate flips is killed in the same server tick, with no tick in which to step off, so the floor it stood on must read as danger BEFORE the beat. It declares no `shown_by` at all. Roof or wall the volume's cells off until the beat that opens them (the beat that arms the volume is usually the beat that should open the way to it); lower the volume so its keep-out's top course lies under the floor a body stands on before the flip; or author one of the blocks vanilla hurts a body with under those cells, visible before the flip, and declare it in `shown_by`. Do not declare the floor a place nobody walks, and do not fire the flag later to pass — a hazard that arrives silently under a body is the finding, wherever on the path it arrives.
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

Built and machine-proven with the engine at `feat/staged-lethal` merged into
the integration branch (`delvec 1.7.1`): two builds byte-identical (97 files);
the prefab expanded twice from the committed program, byte-identical; PackTest
19 of 19, among them `lethal_the_pit` and `lethal_the_pit_shut`. The
mineflayer critical path passes in 5 steps; before each walk it asks the
server whether the pit is live (`lethal/the-pit shut` before the lever,
`live` after it), and its death loop jumps in from the rim, is released 6.92
blocks above the volume, dies at y=66.44 (caught in the volume's course while
still falling, above the points at 65.6875), reads the pit's own line and
reports `staged_live_at_trial` 1 of 1.

The staging gate, with the findings ledger at engine revision 1cd6cd1f, refuses
this build on its own: 2 of 122 findings have no live, binding check on it,
`drill3-01` and `drill3-03`, because the campaign carries no design record.
With the prepared design record copied in, it admits the build: all 122
findings carry a live, binding check or a justified exemption (79 inapplicable).
Not yet walked by a person since the points went in.
