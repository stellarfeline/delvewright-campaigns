# The Heart Under the Floor — design record

The demo level for **a sound that beats over a place** (`pulses[]`, spec-0102).
One mechanic in the spotlight, no cast, about ten minutes.

## The place

A cottage of three rooms in a row, west to east, on a lane at dusk:

| room | what is in it | distance from the hearth |
|---|---|---|
| kitchen (west) | the fireplace in the west wall, and in front of it a raised hearthstone; under the stone, in the floor, the thing that beats | the source |
| parlour (middle) | a bed, a chest, a rug | middle |
| front room (east) | a table and a bench; the front door opens into it from the doorstep | farthest |

The whole cottage is one site-plan place, `node/cottage` (23 x 7 of floor,
one storey, a gabled roof), with the three rooms divided by inner walls and
doorways inside its piece. The doorstep, `node/doorstep`, is open ground under
the sky south of the front room. The party arrives on the doorstep and leaves
from it.

## The beats

1. **Go inside** (`obj/shut-the-door`, a `reach-anchor` in the front room)
   sets `flag/door-shut`. The slow heartbeat starts on that tick, in the
   room farthest from the hearth, at its faintest.
2. **Follow the beat** (`obj/lift-the-hearthstone`, an `interact` at the
   hearthstone) sets `flag/hearthstone-lifted` and takes the stone away. The
   slow beat stops and the fast one starts.
3. **Find what beats** (`obj/find-what-beats`, an `interact` at the same
   place, now an open patch of floor) sets `flag/heart-found`. The beat stops
   within one interval.
4. **Leave** (`obj/walk-out`, a `reach-anchor` on the doorstep) ends the delve.

## The sound

Two pulses on `entity.warden.heartbeat`, both sounding from the cell one under
the hearthstone (`anchor/hearth` + `[0, -1, 0]`), both heard everywhere in
`node/cottage` and nowhere outside it, both with `floor: 0.4`:

| pulse | every | pitch | beats while |
|---|---|---|---|
| `pulse/the-heart` | 30 ticks | 1.0 | `flag/door-shut` and not `flag/hearthstone-lifted` |
| `pulse/the-heart-racing` | 14 ticks | 1.2 | `flag/hearthstone-lifted` and not `flag/heart-found` |

## Branches and endings

None. One ending, on the doorstep.
