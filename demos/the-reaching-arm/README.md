# The Reaching Arm

The demo level for **a strike that locks where the player stands** (spec-0094):
an assembly that, at each wind-up, chooses one player in a region in front of
it, turns to the cell that player stands on, and slams down there with
whichever of its poses comes down on that cell; and a clip the story plays
that holds until the story re-arms the strikes.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-reaching-arm/

and its rig lives in the prefab library, written by the engine's
`prefabs/rig-generator`:

    prefabs/rigs/tentacle/rig.json

## What it is

The yard of *The Thing in the Pit*: a walled yard at noon, a gatehouse at its
south end, a pit at its north end, and a red flag in the middle at
(8211, 64, 8217). Nothing stands in the pit until somebody steps on the flag.

- **The thing** is `rig/tentacle`: thirty-four segments of sculk banded with
  crying obsidian. It comes up when somebody steps on the flag and sways.
- **It locks onto whoever is nearest** on the 9 × 9 of yard round the flag
  (x 8207–8215, z 8213–8221). At the start of each wind-up it reads the cell
  that player stands on, **turns to face it**, leans back, holds, and slams.
- **It has three reaches.** A display entity cannot bend to a point, so the
  limb has three slams the engine chooses among, one per cell: `strike-near`
  for the four rows nearest the pit (35 cells, z 8213–8216), `strike` for the
  middle (37 cells, z 8216–8220), `strike-far` for the far row (9 cells, z
  8221). The turn reaches about 27 degrees either side of straight south.
- **The blow** lands on every cell the chosen slam comes down on — the club
  along the floor through the locked cell, 9 to 18 cells long — and takes 6
  (three hearts). A player who moves off the line during the wind-up and hold
  is not hit.
- **Three sword blows** on its hitbox (a 3 × 8 box rising from the pit) send
  it down into the pit. **It stays down** while anybody stands in front of it.
  Twelve seconds after the third blow it rises again; once it has risen, the
  story re-arms its strikes and it locks onto you again. **Three more blows**
  send it down for good, and it vanishes.

| Thing | Numbers |
| --- | --- |
| Lock region | x 8207–8215, z 8213–8221: 81 cells, every one proved |
| Pick | the player nearest the pit |
| Arming region (`while_in`) | x 8201–8221, z 8210–8224 |
| Wind-up (lean back) | 10 ticks (4 frames at 3), drawn whole on tick 13 |
| Hold | 10 ticks |
| Strike (any reach) | 8 frames at 2; the blow lands on tick 17 |
| Blow | 6 half-hearts, `minecraft:generic` |
| Retract | 180 ticks; held until the story's re-arm |
| Rise again | 240 ticks after the third blow; re-armed 420 ticks after it |

## What to look for

Serve it locally and walk it (below). In order:

1. **Arrive at the gatehouse** with an iron sword. Walk north. Step on the
   red flag: "Something comes up out of the pit." The limb rises and sways.
2. **Stand on the flag.** It turns to you, leans back, holds and slams down
   along the floor onto you. **Watch where the club lands: on you, at the
   moment you take three hearts.**
3. **Walk to the lock region's south-east corner, (8215, 64, 8221).** At the
   next wind-up it **turns to you before it leans back**. Look at the turn:
   **do all thirty-four segments swing round as one thing?** Then it slams
   with its longest reach and lands on you. This is the first thing only a
   client can show.
4. **Walk to the north-west corner, (8207, 64, 8213),** close to the pit. It
   turns the other way and slams with its shortest reach: **does the near
   slam read as a blow, and land on you?**
5. **Stand on a cell and step sideways as it leans back.** The club comes
   down where you were and you take nothing.
6. **Strike the limb three times** from the curb. "It goes back down into the
   dark." **Walk back onto the flag and stay there.** The retract plays to
   the end and the limb stays in the pit: **no wind-up starts over it.** This
   is the defect this level was built to show fixed.
7. **Wait.** "It comes up again." It rises, and once it has finished rising
   it locks onto you and strikes again.
8. **Strike it three more times.** "It goes back down into the dark, and
   stays there." It sinks and vanishes.
9. **Walk back out** to the gatehouse. The delve ends.

The wind-up's length is the creator's: the wind-up clip's frames times its
cadence, then the step's `hold`. Here it is 23 ticks, a little over a second,
from the turn to the blow.

## What the engine refuses (the second half)

Three copies of this campaign, each with one edit, built with the same
engine. The transcripts, verbatim:

**A reach the lock cannot do without** — `reaches` cut to `["strike"]`, so
the far row has no slam that comes down on it:

```
DW0968 [error] build: assembly `assembly/limb`'s strike step 0 can lock onto 9 standable cell(s) of its lock region (/content/assemblies/0/strikes/pattern/0/lock/within) that none of its strike clips (`strike-near`, `strike`) comes down on, turned to face the cell, with its whole blow inside `while_in`: [8207, 64, 8221] [8208, 64, 8221] [8209, 64, 8221] [8210, 64, 8221] [8211, 64, 8221] [8212, 64, 8221] [8213, 64, 8221] [8214, 64, 8221] [8215, 64, 8221]. A display entity does not bend to a point; the lock turns the thing and chooses a pose the rig holds, so a cell no pose reaches is a cell a locked player is never struck on. Why, for the first: [8207, 64, 8221]: `strike-near` does not come down on it; `strike` does not come down on it · [8208, 64, 8221]: `strike-near` does not come down on it; `strike` does not come down on it · [8209, 64, 8221]: `strike-near` does not come down on it; `strike` does not come down on it. Add a clip to `lock.reaches` that comes down there (`delvec rig describe` prints every clip's footprint), shrink the lock region to the cells the clips reach, or widen `while_in`
```

**A lock region past the arming region** — the lock region stretched to nine
cells either side of the flag (`extent` [4, 0, 8]), past both ends of
`while_in`:

```
DW0968 [error] build: assembly `assembly/limb`'s strike step 0 locks onto a player in ([8207, 64, 8209], [8215, 64, 8225]) (/content/assemblies/0/strikes/pattern/0/lock/within), and a body is caught from 18 of its cells outside the arming region `while_in`: [8207, 64, 8209] [8207, 64, 8225] [8208, 64, 8209] [8208, 64, 8225] [8209, 64, 8209] [8209, 64, 8225] [8210, 64, 8209] [8210, 64, 8225] [8211, 64, 8209] [8211, 64, 8225] [8212, 64, 8209] [8212, 64, 8225] [8213, 64, 8209] [8213, 64, 8225] [8214, 64, 8209] [8214, 64, 8225] [8215, 64, 8209] [8215, 64, 8225]. A player who never entered the arming region would be locked onto and struck by a blow that was never wound up for them. Shrink or move the lock region inside `while_in`, or widen `while_in` to cover it
```

**A locked blow given a box of its own** — the blow's `damage-players`
given `in` the flag's cell:

```
DW0969 [error] quests /content/assemblies/0/strikes/pattern/0/on_land/0/in: assembly `assembly/limb`'s strike step 0 locks onto a player, and its `damage-players` (/content/assemblies/0/strikes/pattern/0/on_land/0) declares an `in` box. A locked blow lands on the cells its clip comes down on at the turn it locked to — the compiler derives that area for every cell it can lock, so a written box is a second, fixed answer that is wrong at every other cell. Drop the `in`
```

## Serve it locally

From the engine repository at the branch that carries the lock
(`feat/a-strike-locks-where-the-player-stands`), with this content
repository's worktree as the library:

```
tools/creator/playtest-server.sh up <content>/campaigns/the-reaching-arm --prefabs <content>/prefabs
```

then Multiplayer → Direct Connect `localhost:25565`, pick **Striker**, and walk
the steps above. `tools/creator/playtest-server.sh down` when done.

The staging gate refuses this build: 2 of 122 findings have no live, binding
check on it — `drill3-01` and `drill3-03` (it carries no design record).
Serving it takes the gate's own deliberate override (`--stage-anyway
"<reason>" --acknowledge-red 2`).

## State

Built and machine-proven with the engine at
`feat/a-strike-locks-where-the-player-stands`: `assembly binding: 1
assembl(ies) declared, 34 part(s), 7 clip(s), 1 hitbox(es) examined, 1 strike
step(s) checked over 0 facing(s) and 81 locked cell(s), 0 refused`; PackTest
19 of 19 (among them `asm_hold_limb`: a cued clip with a body in the lock
region begins no wind-up, `arm-strikes` begins one; and `asm_lock_limb_0`:
the dispatch turns the root to the proved yaw at the straight-ahead and the
most-turned cell); the critical-path bot passes all 13 steps — it is struck
for 6 on (8211, 64, 8221) at root yaw −0.04 and again on (8215, 64, 8213) at
root yaw −26.76, is spared outside the arming region at (8199, 64, 8208) for
114 ticks, then strikes the hitbox six times and walks out. Not yet walked by
a person, so the client-side questions above are open.
