# The Tide Mill — design record

The demo level for timed gates (spec-0016 §4): a mill race where the water
gate cycles; the whole level is timing runs through three gates, with
escalating windows.

## Layout

One walled race, `node/race`, six blocks across and thirty-three long, open to
the sky, running north from the sea wall to the mill yard. The west three
blocks are the dry walk; a wall two courses high separates it from the live
channel on the east, two blocks wide and one deep in standing water. The race
walls rise six courses, so nothing is climbed out of.

Three paddle gates cross the walk. Each is a board of spruce planks three wide
and three high, under a headstock of dark oak and stone that spans the race.
They divide the walk into four pounds:

| pound | length | what ends it |
|---|---|---|
| the tail pound, at the sea wall (the party arrives here) | 9 | the first paddle |
| the first pound | 8 | the second paddle |
| the second pound | 8 | the third paddle |
| the head pound | 5 | the head of the race, a gap three wide onto the yard |

North of the race is `node/mill-yard`, a cobbled yard nine across under the
mill's south wall, with barrels against the walls. Reaching it ends the level.

## The paddles

Each paddle is a `timed_gates[]` entry with `crush: true`: it stands shut, lifts
clear for its open half, and drops for its shut half; a body under it when it
drops dies. Every pound is long enough to stand five blocks back from the next
paddle and watch a whole cycle before going.

| paddle | open ticks | shut ticks | share of the cycle a walker can still make it through |
|---|---|---|---|
| first | 80 | 40 | 60% |
| second | 50 | 50 | 43% |
| third | 30 | 70 | 23% |

The share is `DW0378`'s arithmetic over the one-block span: two moves at four
ticks a block.

## Beats

1. The party arrives in the tail pound.
2. Through the first paddle into the first pound (`obj/first-paddle`; a
   checkpoint there).
3. Through the second paddle into the second pound (`obj/second-paddle`; a
   checkpoint).
4. Through the third paddle into the head pound (`obj/third-paddle`; a
   checkpoint).
5. Up into the mill yard (`obj/mill-yard`), and the campaign completes.

No branch, no ending table, no cast.
