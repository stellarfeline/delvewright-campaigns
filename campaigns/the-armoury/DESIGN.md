# The Armoury — design record

A demo level for item holders: an item sits where the scene would hold it —
on an armour stand, in a frame, in a chest — and a player in adventure mode
takes it by the game's own act, without being able to take or break the thing
that held it.

## The place

Greyholt, a stone watch-house on a moor road. Two places, both on one ground.

| place | what stands in it | holders |
|---|---|---|
| the yard | flagstones inside a wall the moor shows over; a lamp post; the armoury door in its north wall | none |
| the armoury | one stone room with a plank floor, a lantern overhead; a bench and a grindstone on the east wall | a rack of three armour stands along the west wall; a glow frame on the door wall, east of the door; a chest under the window in the north wall |

The armoury's holders, north to south along the west wall, then the door wall
and the window wall:

| holder | what it holds | slot | who fills it |
|---|---|---|---|
| the north stand | a shield | `weapon.offhand` | `loot` |
| the middle stand | the post sword | the quest's | `collect` (the quest item) |
| the south stand | an iron helmet | `armor.head` | `loot` |
| the glow frame beside the door | a map of the moor road | `contents` | `loot` |
| the chest under the window | arrows, and nothing else | `container.0`, `container.1` | `loot` |

Every holder in the room holds something; no holder is empty and no
container is scenery.

## Beats

1. **Arrival.** The class is chosen; the party stands in the yard with the
   armoury door ahead and the warden beside it.
2. **Meet Ide Fenwick.** She is handing the post over and going down to the
   valley; the post goes with its sword, which is on the rack inside. Whatever
   else hangs in there is the watch's, and the watch is the party now.
3. **The armoury.** The rack, the frame by the door, the chest under the
   window. The sword is taken from its stand.
4. **Bring the sword out** to Ide in the yard. She hands over the post and
   goes; the outro plays.

No branch, no fight, no death. One player is enough; more walk together.
