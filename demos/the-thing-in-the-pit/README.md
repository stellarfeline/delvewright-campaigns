# The Thing in the Pit

The demo level for **a fixed thing that can be hit and hits back** (spec-0082):
an assembly of display entities standing at a mark, playing the clips of a
library rig, struck in melee through its hitbox, and striking a player who
stands where its blow comes down.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-thing-in-the-pit/

and its rig lives in the prefab library, written by the engine's
`prefabs/rig-generator`:

    prefabs/rigs/tentacle/rig.json

## What it is

A walled yard at noon, with a gatehouse at its south end and a pit at its north
end. Nothing stands in the yard until somebody steps on the red flag in its
middle.

- **The gatehouse** (around 8211, 64, 8244) is where you arrive and where you
  walk back out to.
- **The red flag** is one block of red concrete at (8211, 64, 8217), in the
  middle of the yard.
- **The pit** is a 3 × 3 floor of sculk inside a one-block curb of polished
  blackstone, centred on (8211, 64, 8205), twelve blocks north of the flag.
  The curb is a step, not a wall: you can walk in and out.
- **The thing** is `rig/tentacle`: thirty-four segments of sculk banded with
  crying obsidian, thick from the base to a club and then tapering to a thin
  tip. It comes up when somebody steps on the flag and sways. While anybody
  stands in the strip of yard in front of it, it **turns to face whoever is
  nearest**, leans back, holds, and **slams down along the floor toward them**:
  it arches over head height out of the pit and lays its club flat along the
  ground from nine to fifteen blocks in front of the pit, the tip curling up at
  the end. A body standing where the club comes down takes 6 (three hearts).
  Five sword blows on it send it back down into the pit, where it vanishes.

| Thing | Numbers |
| --- | --- |
| Facings it can turn to | 8, evenly spaced; the three a player in front of it can make it take: straight south, south-east and south-west |
| Wind-up (lean back) | 10 ticks (4 frames at 3 ticks each; drawn whole on tick 13) |
| Hold | 6 ticks |
| Strike (the slam) | 8 frames at 2 ticks; the blow lands on tick 17, when the last frame is drawn whole |
| Blow | 6 half-hearts, `minecraft:generic` |
| Where the blow lands (straight south) | the seven cells from (8211, 64, 8214) to (8211, 64, 8220), the flag in the middle, and a body standing in the cell beside any of them that reaches into it |
| Where the blow lands (south-east, south-west) | the same seven cells' length turned an eighth of a turn about the pit: four cells along each diagonal, from about (8218, 64, 8212) / (8204, 64, 8212) outward |
| Arming region | x 8201–8221, z 8212–8222: the strip of yard from seven blocks in front of the pit to five past the flag |
| Blows to send it down | 5 |

## What to look for

Serve it locally and walk it (below). In order:

1. **Arrive at the gatehouse** with an iron sword. Walk north into the yard.
   Nothing is in the pit.
2. **Step on the red flag.** "Something comes up out of the pit." The limb
   stands in the pit and sways. Look north at it: **does it read as one body**,
   moving as one thing between keyframes, or as thirty-four blocks jittering?
3. **Stay on the flag.** It leans back for half a second, holds, then arches
   over and slams down along the floor straight at you. **Watch where the club
   lands: it should lie along the ground through the flag, on you, at the
   moment you take three hearts** — not before it arrives, and not beside you.
4. **Walk to (8218, 64, 8212)**, south-east of the pit. At the next wind-up it
   **turns to face you** before it leans back. **Look at the turn: do all
   thirty-four segments swing round together as one thing**, with no segment
   left behind or torn from the rest? Then it slams down along the diagonal
   onto you. This is the first thing only a client can show.
5. **Step three blocks east of the flag line**, to (8214, 64, 8217). It still
   faces straight south (you are nearest that facing) and slams down along the
   flag's line; **the club lands beside you and you take nothing.**
6. **Step back past the arming region**, to (8199, 64, 8210) beside the pit's
   south-west corner. It finishes the blow it was making and stops; it does not
   wind up again until somebody comes back in front of it.
7. **Walk to the pit and strike the limb** with the sword, from the curb. Each
   blow lands on its hitbox (a 3 × 8 box rising from the pit). **Look at where
   you are hitting**: the hitbox stands on the root at the pit's centre, not on
   the parts — the second thing only a client can show is whether a part
   riding the root draws where the server keeps it.
8. **Try a bow** from the yard: the arrow passes straight through. The thing is
   struck in melee only.
9. **The fifth blow** sends it down: "It goes back down into the dark." It sinks
   into the pit over nine seconds and is gone.
10. **Walk back out** to the gatehouse. The delve ends.

The wind-up's length is the creator's: the wind-up clip's frames times its
cadence, then the step's `hold`; a step's `ticks_per_frame` would play the same
clips faster or slower. The engine sets no floor on it.

## What the engine refuses (the second half)

Four copies of this campaign, each with one edit, built with the same engine.
These are the transcripts, verbatim; where a refusal is raised at several
facings, the straight-south one is shown and the count of the others given.

**One cell where the club comes down along seven** — the landing box shrunk to the flag's own cell (`extent` [0, 0, 0]), the blow the old level dealt: Refused at 3 facing(s) in all; the others name their own cells.

```
DW0938 [error] build: assembly `assembly/limb`'s strike step 0: the strike clip `strike` comes down on 8 standable cell(s) at facing 0 of 8 (turned 0 degrees from the declared facing, root yaw 0) its blow (/content/assemblies/0/strikes/pattern/0/on_land/0) does not land on — its last frame meets a body standing there within 1 block of the floor, its first frame did not, and the body is not caught by the landing box even by the box's edge (its keep-out, one cell round it for a player): [8210, 64, 8215] [8210, 64, 8219] [8211, 64, 8214] [8211, 64, 8215] [8211, 64, 8219] [8211, 64, 8220] [8212, 64, 8215] [8212, 64, 8219]. The blow's area must be the area the limb comes down on; a long limb's blow is a long area along where it lands. Widen the landing box to cover them (`delvec rig describe` prints the footprint), or choose a strike clip that comes down only where the blow lands
```

**A blow the limb never comes down on** — the step strikes with `windup` (the lean back) instead of `strike`, so nothing comes down in front of the pit: Refused at 3 facing(s) in all; the others name their own cells.

```
DW0938 [error] build: assembly `assembly/limb`'s strike step 0 lands a blow (/content/assemblies/0/strikes/pattern/0/on_land/0) at facing 0 of 8 (turned 0 degrees from the declared facing, root yaw 0) on 7 standable cell(s) the strike clip `windup` never comes down on — on its last frame, drawn whole when the blow lands, no part meets a body standing there within 1 block of the floor (the body's own width round the cell's centre): [8211, 64, 8214] [8211, 64, 8215] [8211, 64, 8216] [8211, 64, 8217] [8211, 64, 8218] [8211, 64, 8219] [8211, 64, 8220]. The thing the player saw come down must be the thing that hurt them. Where the last frame comes down on a standing body: [8210, 64, 8204] [8210, 64, 8205] [8210, 64, 8206] [8211, 64, 8204] [8211, 64, 8205] [8211, 64, 8206] [8212, 64, 8204] [8212, 64, 8205] [8212, 64, 8206]. Move the landing box under the limb (`delvec rig describe` prints the footprint), or choose a strike clip that comes down on it
```

**A landing box outside the arming region** — the landing box lengthened to thirteen cells (`extent` [0, 0, 6]), past the arming region's south edge: Refused at 3 facing(s) in all; the others name their own cells.

```
DW0938 [error] build: assembly `assembly/limb`'s strike step 0 lands a blow (/content/assemblies/0/strikes/pattern/0/on_land/0) at facing 0 of 8 (turned 0 degrees from the declared facing, root yaw 0) whose box catches a body from the feet cells [8210, 63, 8210]..=[8212, 64, 8224], and the arming region `while_in` catches one only from [8200, 62, 8211]..=[8222, 65, 8223]. A player who never entered the arming region would be struck by a blow that was never wound up for them. Shrink or move the landing box inside `while_in`, or widen `while_in` to cover it
```

**A hitbox too wide for vanilla to register across** — `hitbox.width` 7:

```
DW0936 [error] build: assembly `assembly/limb` (/content/assemblies/0/hitbox/width) declares a hitbox 7 wide. Vanilla detects an attack on a `minecraft:interaction` only within 3.3 blocks of its position toward -X and -Z (Minecraft Wiki, Interaction), so a box wider than 6 has a slab no swing registers on. Declare a width over 0 and at most 6
```

## Serve it locally

From the engine repository at the branch that carries assemblies
(`feat/display-assembly`), with this content repository's worktree as the
library:

```
tools/creator/playtest-server.sh up <content>/campaigns/the-thing-in-the-pit --prefabs <content>/prefabs
```

then Multiplayer → Direct Connect `localhost:25565`, pick **Striker**, and walk
the steps above. `tools/creator/playtest-server.sh down` when done. The level
is never copied into a singleplayer save.

The staging gate refuses this build: 2 of 122 findings have no live, binding
check on it — `drill3-01` and `drill3-03` (it carries no design record).
Serving it takes the gate's own deliberate override (`--stage-anyway
"<reason>" --acknowledge-red 2`).

## State

Built and machine-proven with the engine at `feat/display-assembly`: two
builds byte-identical; the strike judged at the 3 facings a player in front of
it can draw, 0 refused; PackTest 17 of 17; the critical-path bot passes all 11
steps — it stands on (8211, 64, 8214), under the club, and is struck for 6;
stands outside the arming region at (8199, 64, 8210) for 106 ticks and takes
nothing; then strikes the hitbox five times and walks out. The bot witnesses
the straight-south facing only; the diagonal facings are proved by the
compiler and are looked at in step 4. Not yet walked by a person, so the
client-side questions above are open.
