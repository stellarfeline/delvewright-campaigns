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
  middle of the yard, with a short stone-brick kerb on its west side.
- **The pit** is a 3 × 3 floor of sculk inside a one-block curb of polished
  blackstone, centred on (8212, 64, 8200), seventeen blocks north of the flag.
  The curb is a step, not a wall: you can walk in and out.
- **The thing** is `rig/tentacle`, the research spike's 34-segment limb of
  sculk banded with crying obsidian. It comes up when somebody steps on the
  flag, sways, and — while anybody stands on or beside the flag — leans back,
  holds, and arcs over the yard to bring its tip down on the flag. A body on
  the flag takes 6 (three hearts). Five sword blows on it send it back down
  into the pit, where it vanishes.

| Thing | Numbers |
| --- | --- |
| Wind-up (lean back) | 36 ticks, 8 frames at 5 ticks each |
| Hold | 20 ticks |
| Strike (the arc) | 46 ticks, 10 frames at 5 ticks each |
| Blow | 6 half-hearts, `minecraft:generic`, on the flag's cell |
| Arming region | the 5 × 5 round the flag (`while_in` extent 2) |
| Blows to send it down | 5 |

## What to look for

Serve it locally and walk it (below). In order:

1. **Arrive at the gatehouse** with an iron sword. Walk north into the yard.
   Nothing is in the pit.
2. **Step on the red flag.** "Something comes up out of the pit." The limb
   stands in the pit and sways. Look north at it: **does it read as one body**,
   moving as one thing between keyframes five ticks apart, or as thirty-four
   blocks jittering? This is the first of the three things no server and no bot
   can see — interpolation is drawn by your client.
3. **Stay on the flag.** It leans back (the wind-up), holds for a second, then
   arcs over the yard and comes down on you. You take three hearts. Watch where
   the tip lands: it should come down on the flag, not beside it.
4. **Step one block east of the flag** (8213, 64, 8217) and wait for the next
   blow. It still winds up and strikes — you are inside the arming region —
   but the blow does not land on you.
5. **Step back past the arming region** (three or more blocks from the flag).
   It finishes the blow it was making and stops; it does not wind up again
   until somebody comes back.
6. **Walk north to the pit** and strike the limb with the sword, from the curb.
   Each blow lands on its hitbox (a 3 × 8 box rising from the pit). **Look at
   where you are hitting**: the hitbox stands on the root at the pit's centre,
   not on the parts — the second thing only a client can show is whether a
   part riding the root draws where the server keeps it.
7. **Try a bow** from the yard: the arrow passes straight through. The thing is
   struck in melee only.
8. **The fifth blow** sends it down: "It goes back down into the dark." It sinks
   into the pit over nine seconds and is gone.
9. **Walk back out** to the gatehouse. The delve ends.

The third thing only a client can show — whether a one-frame wind-up reads as
a blow or as a glitch — this level does not show: its wind-up is eight frames.
Wind-up length is the creator's to choose and the engine sets no floor on it.

## What the engine refuses (the second half)

Three copies of this campaign, each with one edit, built with the same engine.
These are the transcripts, verbatim.

**A landing box the limb never reaches** — the step strikes with `windup` (the
lean back) instead of `strike`, so nothing comes down on the flag:

```
DW0938 [error] build: assembly `assembly/limb`'s strike step 0 lands a blow (/content/assemblies/0/strikes/pattern/0/on_land/0) on 6 standable cell(s) the strike clip `windup` never reaches — no part stands in the column from the cell's floor to 3 above it on the clip's last frame: [8211, 64, 8216] [8211, 64, 8217] [8211, 64, 8218] [8212, 64, 8216] [8212, 64, 8217] [8212, 64, 8218]. The thing the player saw come down must be the thing that hurt them. Where the clip's last frame stands from that floor to 3 above it: [8210, 64, 8198] [8210, 64, 8199] [8210, 64, 8200] [8210, 64, 8201] [8210, 64, 8202] [8210, 65, 8198] [8210, 65, 8199] [8210, 65, 8200] [8210, 65, 8201] [8210, 65, 8202] [8210, 66, 8198] [8210, 66, 8199] [8210, 66, 8200] [8210, 66, 8201] [8210, 66, 8202] [8211, 64, 8198] [8211, 64, 8199] [8211, 64, 8200] [8211, 64, 8201] [8211, 64, 8202] [8211, 65, 8198] [8211, 65, 8199] [8211, 65, 8200] [8211, 65, 8201], and 63 more. Move the landing box under the limb (`delvec rig describe` prints the footprint), or choose a strike clip that reaches it
```

**A landing box outside the arming region** — the arming region shrunk to the
flag's own cell and the landing box widened to the three cells across it:

```
DW0938 [error] build: assembly `assembly/limb`'s strike step 0 lands a blow (/content/assemblies/0/strikes/pattern/0/on_land/0) whose box catches a body from the feet cells [8209, 63, 8216]..=[8213, 64, 8218], and the arming region `while_in` catches one only from [8210, 63, 8216]..=[8212, 64, 8218]. A player who never entered the arming region would be struck by a blow that was never wound up for them. Shrink or move the landing box inside `while_in`, or widen `while_in` to cover it
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

The staging gate refuses this build: 4 of 122 findings have no live, binding
check on it — `isl-35` and `isl-46` (no cast is declared over its one quest),
`drill3-01` and `drill3-03` (it carries no design record). Serving it takes the
gate's own deliberate override (`--stage-anyway "<reason>" --acknowledge-red 4`).

## State

Built and machine-proven with the engine at `feat/display-assembly`: two
builds byte-identical; PackTest 17 of 17; the critical-path bot passes all 9
steps, striking the hitbox five times. Not yet walked by a person, so the
three client-side questions above are open.
