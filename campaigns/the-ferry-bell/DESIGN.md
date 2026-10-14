# The Ferry Bell — design

The demo level for **guidance a player can follow** (spec-0104): every act is
in sight of the last one or announced with a hint; every title opens with the
verb its kind completes on, in English and in Chinese; the opening teaches each
input it will need, in the keeper's own voice, with the key shown as the
player's own binding; the thing to press stands alone among its kind; and
nothing in the level carries a marker.

## The place

One sandy shore in the rain, on the south side of a small cove that opens to
the sea on the north and west. Grid: x east, z south; the walk plane is y 64.

| place | box | what it is |
|---|---|---|
| `node/shore` (entry) | x 8196–8235, z 8209–8218, open | the beach at the jetty foot: Nell stands west of the jetty mouth, the ferry notice on its post east of it, a lamp post either side of the mouth; an upturned boat, crates and a barrel on the sand; a sand step down to the shallows west of the jetty, a fence along the water east of it and down the beach's east edge |
| `node/jetty` | x 8209–8211, z 8192–8207, hung over the shallows | a plank jetty three wide with a spruce rail along both sides and a lantern on the rail at each end, running sixteen blocks out to the ferry-house door; the bolt lever on the deck beside the door |
| `node/ferry-house` | x 8207–8213, z 8185–8190, hung over the cove, roofed | a small timber house at the jetty's end under a gabled dark-oak roof; a plank door in its south wall, bolted; the ferry bell on its floor frame in the middle of the house; a one-course slit window in the east wall over the cove, a glazed window in the west wall, two hanging lanterns |
| `node/far-bank` | x 8226–8235, z 8186–8207, open | the spit of sand that closes the cove on the east, joined to the shore at its root, fenced along its other three edges where nets are dried; driftwood and dry bushes; the dead form up at its west edge, facing the ferry house across nine blocks of water |

The water is the cove: six courses deep, with three cells of shallows at the
foot of each bank. The sea outside the region is the ocean horizon.

## The beats, in order

| # | act | kind | input class | found by |
|---|---|---|---|---|
| 1 | talk to Nell at the jetty foot | `talk-to` | use-body | sight, from the spawn |
| 2 | read the ferry notice on its post | `interact`, sign prop | use-block | sight, from Nell |
| 3 | pull the bolt lever by the ferry-house door | `interact`, lever prop | use-block | sight, from the notice, along the jetty |
| 4 | ring the ferry bell inside the house | `interact`, bell prop | use-block | a hint (the bell is inside, behind the door) |
| 5 | fight off the dead that form up on the spit | `kill` | attack-body | sight through the east slit and the dead's reach (`follow_range` 24) |

Ringing the bell sets the party's checkpoint on the jetty. The quest completes
on the last of the dead, and the campaign ends: the outro says the ferry is
coming.

## Teaching

`guidance.teaching` carries three lines in Nell's voice, one per input class
the walk needs: `use-body` (shown when talking to Nell is first the next thing
to do), `use-block` (shown when the notice is), `attack-body` (shown when the
fight is). `attack-block` is not declared, because no act needs it.

## The refusal the level is built to show

The lever is first built on the jetty rail, among the rail's spruce fence
posts, and refused. It is then moved off the rail to the deck beside the door.
The README records the refusal and two variants of it.

## Hour and weather

Day, in rain. The rain is what lets the dead — zombies — stand on open sand by
day without burning (`DW0496`), and it is the weather the level is about.
