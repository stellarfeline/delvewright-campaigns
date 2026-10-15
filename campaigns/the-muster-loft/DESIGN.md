# The Muster Loft — design

A demo level for one mechanic: a connection the story shuts is built shut. Every
way out of the hall stands barred in blocks from world load, and each bar comes
up at the beat that opens it. Ten to twenty minutes, one class, no speaking
cast.

## The places

Four places cut into the hill under Harrowgate, every one roofed, the rock
round them solid.

| place | what it is | floor |
|---|---|---|
| `node/hall` | the muster hall: the spawn, the fight, the hub every way leaves from | 64 |
| `node/loft` | the loft where the levy's names are kept, north of the hall and above it | 69 |
| `node/stores` | the stores room, through a door in the hall's east wall | 64 |
| `node/cellar` | the cellar under the hall and the stores | 60 |

## The connections

| connection | class | shut until | how it reads shut |
|---|---|---|---|
| `edge/loft-stair` hall → loft | `stair`, treads in the hall | the muster falls | bars across the passage at the stair's head |
| `edge/cellar-shaft` hall → cellar | `drop`, 4 down | the muster falls | a hatch of bars over the shaft in the hall floor |
| `edge/cellar-stair` stores → cellar | `stair`, treads in the cellar | the muster falls | a hatch of bars over the stairwell in the stores floor |
| `edge/cellar-ladder` cellar → hall | `climb`, up through the hall floor | the grating is drawn, from the hall only (`opens_from` the hall) | a grating standing on the hall floor over the ladder's hole; the hole keeps the top rung |
| `edge/stores-door` hall ↔ stores | `walk` | never shut | an open doorway |

The ladder is the shortcut (`shortcut: true`): it closes the loop hall → shaft →
cellar → ladder → hall. The stores stair is the long way round: out of the
cellar by the stores, through the stores door, back into the hall.

Before the muster falls, a body in the hall reaches the stores and nothing else;
the loft and the cellar are behind bars on every side. That is what `DW1011`
proves for the stair, the shaft and the stores stair. The ladder's grating is a
declared shortcut, which `DW1011` counts and does not judge: once the muster
falls the cellar is open by two other ways, so the grating separates nothing
the story needs; what it does is make the ladder one-sided until it is drawn.

## The beats, in order

1. **Arrival** (`quest/the-bars`, campaign start). The party arrives in the hall,
   which is empty. A narration says the levy falls in at dusk and the bars hold
   until it falls. Four objectives walk the party to each shut way:
   - try the loft stair — climb to its head and meet the bars (`anchor/stair-head`);
   - look down the cellar hatch (`anchor/hatch-rim`);
   - try the grating over the cellar ladder (`anchor/unlock-cellar-ladder`);
   - try the stores stair — through the stores door, the hatch over the stairwell
     (`anchor/node-stores`).
2. **The muster** (`quest/the-muster`). With the four tried, the dead levy falls
   in on the hall floor (`wave/the-levy`, three zombies). Put it down. When it
   falls, `flag/muster-fallen` is set and three bars come up together: the loft
   stair's head, the cellar hatch, the stores stair's hatch. The grating stays.
3. **The roll** (`quest/the-roll`). Drop through the hatch into the cellar and
   take the muster roll from the chest on its shelf (`anchor/roll-shelf`). Try the
   ladder (`anchor/ladder-foot`): it climbs to its top rung and stops under the
   grating. The way out is the long way round: up the stores stair, through the
   stores door, into the hall. Draw the grating from the hall
   (`anchor/unlock-cellar-ladder`, an `interact`): it comes up, `flag/grating-drawn`
   is set, and the ladder is the short way into the cellar from then on.
4. **The loft** (still `quest/the-roll`). Climb the loft stair and lay the roll in
   the loft (`anchor/node-loft`). The levy is stood down; the delve ends.

Critical path: hall → stores → hall → cellar → stores → hall → loft.

## What the owner judges

- Does a bar at the head of a stair, a hatch over a shaft and a grating over a
  ladder each read as a way the story will open?
- Does each open at its beat — three at the muster's fall, the grating when it is
  drawn?
- Does the ladder's top rung under the grating feel like the stop it is?

## Branches and endings

None. One ending, the roll laid in the loft.
