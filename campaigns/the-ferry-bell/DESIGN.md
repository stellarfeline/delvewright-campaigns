# The Ferry Bell — design

The demo level for **guidance a player can follow** (spec-0104): every act is
in sight of the last one or announced with a hint; the compass each player
carries follows an open objective, and right-clicking it opens the list of the
open objectives to pick from; a lever that does not read as the door's bolt
glows while a player is near it; and the journal in every hand holds the
engine's compass page, the keeper's notes, the open objectives and the done
ones.

## The place

One sandy shore in the rain, on the south side of a small cove that opens to
the sea on the north and west. Grid: x east, z south; the walk plane is y 64.

| place | box | what it is |
|---|---|---|
| `node/shore` (entry) | x 8196–8235, z 8209–8218, open | the beach at the jetty foot: Nell stands west of the jetty mouth, the ferry slate on its post east of it at the jetty's head, a lamp post either side of the mouth; an upturned boat, crates and a barrel on the sand; a sand step down to the shallows west of the jetty, a fence along the water east of it and down the beach's east edge |
| `node/jetty` | x 8209–8211, z 8192–8207, hung over the shallows | a plank jetty three wide with a spruce rail along both sides and a lantern on the rail at each end, running sixteen blocks out to the ferry-house door; the bolt lever on the deck beside the door |
| `node/ferry-house` | x 8207–8213, z 8185–8190, hung over the cove, roofed | a small timber house at the jetty's end under a gabled dark-oak roof; a plank door in its south wall, bolted; the ferry bell on its floor frame in the middle of the house; a one-course slit window in the east wall over the cove, a glazed window in the west wall, two hanging lanterns |
| `node/far-bank` | x 8226–8235, z 8186–8207, open | the spit of sand that closes the cove on the east, joined to the shore at its root, fenced along its other three edges where nets are dried; driftwood and dry bushes; the dead form up at its west edge, facing the ferry house across nine blocks of water |

## The beats

| # | act | kind | told | found by |
|---|---|---|---|---|
| 1 | talk to Nell at the jetty foot | `talk-to` | announced | sight, from the spawn |
| 2 | read the ferry slate at the jetty's head | `interact`, dark-oak sign prop | announced, with a hint | opens with 3, when the talk ends |
| 3 | ring the ferry bell inside the house | `interact`, bell prop | announced, with a hint | the hint (the bell is inside, behind the bolted door) |
| — | pull the bolt lever by the ferry-house door | `interact`, lever prop, `highlight {within: 6}` | not announced: no title, so no compass, no journal page | sight, from the slate, along the jetty |
| 4 | fight off the dead that form up on the spit | `kill`, after the bell | announced | sight through the east slit and the dead's reach (`follow_range` 24) |

Talking to Nell opens the slate and the bell at once, so two objectives are
open together and each player's compass follows the one they pick: at Nell's
side the slate is a few steps to one side and the bell straight out along the
jetty. The lever opens with them, unannounced: it is the way to the bell, which
the bell's hint names, and it glows only while a player is within six blocks of
it — the last stretch of the jetty deck. The bell carries no highlight, because
a bell reads as a bell. The bell sets the party's checkpoint on the jetty and
calls the fight. The quest completes when every objective is done, and the
campaign ends: every compass spins and every journal holds only done pages.

## The journal

`guidance.manual` carries two pages in Nell's voice under the title *The
Ferry-Keeper's Notes*: the first says how the ferry-house bolt is drawn, with
the use key as the player's own binding (`[[key|use]]`), the second what the
bell calls. The engine's compass page comes first; the open and done pages are
derived from the objectives.

## The refusal the level is built to show

The lever is first built on the jetty rail, among the rail's spruce fence
posts, and refused by `DW0863`: from the slate, the next post hides it, and an
act nobody announces has no hint to fall back on. It is moved off the rail to
the deck beside the door.

## Hour and weather

Day, in rain. The rain is what lets the dead — zombies — stand on open sand by
day without burning (`DW0496`), and it is the weather the level is about.
