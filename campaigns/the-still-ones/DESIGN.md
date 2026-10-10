# The Still Ones — design

The demo level for **a body that watches** (spec-0101): a still body turns to
face the nearest player within its reach, holds its last look when nobody is
in reach, and yields the turn to any walk the story gives it.

## The place

Lantern Row at dusk, under a clear sky. One site plan, one area (`area/site`).

| place | what it is | box |
|---|---|---|
| `node/gate` | the bottom of the row: a gap in a hedge where the party comes in | 5 × 5, open |
| `node/row` | the street: cobbles five wide, 28 long, between plastered timber fronts, torches between the doors | 5 × 28, open |
| `node/tailors` | first door on the left: the tailor's front room, a loom at the back | 3 × 3, roofed |
| `node/coopers` | the door on the right: the cooper's shop, barrels at the back | 3 × 3, roofed |
| `node/watch-house` | last door on the left: the old watch-house, stone, a lectern | 3 × 3, roofed |
| `node/square` | the top of the row: a paved square with a well in the middle and a lantern at each corner, ringed by hedge | 11 × 9, open |

Each house's open double door is in the row's frontage. The figure of each
house stands on the cell just inside its door, framed by it, facing the
street.

## The cast

| body | class | where | watches |
|---|---|---|---|
| `actor/the-tailor` | actor, skinned mannequin (`skins/tailor.png`) | inside the tailor's door | the nearest player within 7 |
| `actor/the-dry-one` | actor, a plain husk | inside the cooper's door | the nearest player within 7 |
| `actor/the-keeper` | actor, a plain villager holding a lantern (a warder's, as the Warder class carries) | inside the watch-house door | the nearest **warder** within 8 |
| `npc/the-reeve` | NPC, skinned mannequin (`skins/annick.png`) | the top of the row, then by the well | the nearest player within 10 |

The three actors are summoned when the first player comes within 4 of the
gate (`trigger/dusk-on-the-row`). The reeve stands at the top of the row
from world load.

## The beats

1. **The gate.** The party chooses a class — Warder or Traveller — and comes
   in at the bottom of the row. "Someone stands in every door."
2. **The row.** Walking up the street, each figure turns to face whoever of
   the party is nearest while they are in its reach, and holds its last look
   once they pass out of it. The keeper of the watch-house turns only to a
   warder; a traveller walks past him unseen.
3. **The reeve walks.** When a player comes within 7 of the top of the row
   (`trigger/the-reeve-walks`, an `approach` trigger), the reeve turns and
   walks up into the square, round the well, and stops on its far side
   (`anchor/by-the-well`). She does not watch while she walks; from where she
   stops she watches again. `obj/walk-the-row` completes at the top of the
   row (radius 2).
4. **The well.** The party speaks with the reeve (`obj/hear-the-reeve`): who
   the still ones are, why they watch, why the keeper looks only at a warder.
   "Then we've been seen" completes the quest and the delve.

No combat, no fail state, one ending.

## The one mechanic, and what is not in this level

Nothing in the level is there except to show the watch: four bodies, both
body classes, both `who` shapes, the mannequin and the mob branch, one walk.
Two players are needed to see a figure choose between them; one is enough for
everything else.
