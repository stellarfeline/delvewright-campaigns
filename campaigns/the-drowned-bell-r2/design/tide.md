# The Drowned Bell — the tide

The sea is a level, and it moves. This document is the campaign's design of that
movement: what the level is, when it steps, what each step changes, and where it
deliberately changes nothing.

## The rule the design obeys

**One plane, whole-world, moved all at once.** Halgrave has exactly one water
level at any moment and every zone reads the same one. No column ever has a
lower neighbour to drain into, because nothing is ever lower than anything else
— the plane moves, the world does not.

Two consequences the design is built around, not around which it works:

- **No bounded basin.** There is no pool, tank or flooded room in this campaign
  that holds a level of its own. Everything wet is the sea, reached through a
  broken wall, a gate, a well or the rock's own fissures. A basin that tried to
  hold its own level would be re-flooded from its edges within the minute, so
  the design does not contain one.
- **Every wet volume is solid water, and there are no air pockets under the
  plane.** A void below the level is full, by construction, corner to corner. So
  the delve never offers a dive that surfaces into a drowned room, and any space
  the player is meant to breathe in is above the plane at every step the player
  can be standing in it.

**Flowing water is not used.** The gate passage's channel (`Z2`) reads as a
running drain through its fall, its wet stone and its weed, and it is still
water at the plane's height or a dry gutter — never a flow. This is a deliberate
departure from the literal reading of `concept/z2-gatehouse.jpg`, taken because
a running channel is a lie the physics cannot keep, and a brimming gutter that
empties over the run tells the same story better.

## The night

The delve is one night of two ebbs, and the second is the lowest water in
fifty-one years. That is why tonight is the night: **the bell's tongue has been
under water since the day it was thrown down the well, and it clears the surface
for about two hours, once in a lifetime, tonight.** Nothing else about the rock
has changed. The delve exists because of a tide table.

## The levels

Heights are relative to the standing tide, the level the sea has held since the
winter after the Long Tide. `0.0` is that level.

| id | name | height | what it is |
|---|---|---|---|
| `T-EBB1` | the first ebb | −2.0 | the night's first low water. The delve opens here. |
| `T-STAND` | the standing tide | 0.0 | ordinary water. The level the coast has lived under for fifty-one years. |
| `T-FLOOD` | the flood | +2.0 | the night's high water, at the delve's middle. |
| `T-DEAD` | the Dead Ebb | −2.5 | the lowest water in fifty-one years. The delve ends here. |

Four levels, four steps, one direction each. There is no fifth.

## The rock against the plane

Floor heights, so that a single plane produces the whole delve. Everything
above `+2.0` is never touched by water in any state.

| feature | height | `T-EBB1` | `T-STAND` | `T-FLOOD` | `T-DEAD` |
|---|---|---|---|---|---|
| Barrow flat (Z0) | −1.2 | dry | under | under | dry, and lower than anyone has seen |
| cliff road, main ledge (Z1) | +4.0 | dry | dry | dry | dry |
| cliff road, the K2 gap (Z1) | +2.0 | air | air | **at the water** | air |
| gate passage floor (Z2) | +2.5 | dry | dry | dry | dry |
| gate passage channel invert (Z2) | +1.8 | dry gutter | dry gutter | **brimming** | dry gutter |
| drowned ward floor (Z3) | −1.5 | 0.5 dry | 1.5 deep | 3.5 deep | **1.0 dry — walkable** |
| ward causeway top (Z3) | +0.4 | dry | dry | **awash** | dry |
| cistern floor (Z6) | −0.15 | dry | **ankle-deep** | 2.2 deep | dry |
| cistern supply channel invert (Z6) | −2.6 | water | water | water | water |
| the well shaft's silt bed (Z6) | −2.3 | under | under | under | **clear by 0.2** |
| chapel ward (Z4) | +9 | — | — | — | — |
| hall floor (Z5) | +12 | — | — | — | — |
| tower approach and belfry (Z7) | +14 / +30 | — | — | — | — |

Two rows carry the whole design. The **ward floor** is walkable at the Dead Ebb
and at no other time, which turns the delve's most familiar zone into a new one
at the end. The **well shaft's silt bed** clears the Dead Ebb by twenty
centimetres, which is the entire reason there is a delve.

The **supply channel** is under water at every level including the Dead Ebb.
That is deliberate: `K5`'s tell — a black band in the reflection of the light
shaft — is true at every state of the tide, so the delve never teaches a rule
that a later step breaks.

## The steps

Four steps, each bound to a critical-path node. **No step is bound to a wall
clock.** The player can spend an hour anywhere and the sea will not move until
they move the story, which keeps exploration free and keeps the schedule
machine-checkable: four steps, one order, one direction each.

| step | fires at | plane goes | authored so that |
|---|---|---|---|
| `TIDE-1` | **CP-07**, the portcullis finishes rising | `T-EBB1` → `T-STAND` | the player is at the winch, looking down the gate passage at the shore they walked in from. They see it go. |
| `TIDE-2` | **CP-12**, the banded door is unbarred | `T-STAND` → `T-FLOOD` | the door swings and the view through it is the drowned ward, going under, on the route they will now never have to walk again. |
| `TIDE-3` | **CP-15**, entering the descent from the keep | `T-FLOOD` → `T-STAND` | the descent stair's lower flight is running wet as they come down it — the sea is leaving ahead of them. |
| `TIDE-4` | **CP-16**, the Founder goes down | `T-STAND` → `T-DEAD` | he falls in ankle-deep water beside the well, and the water goes out from under him. |

Every step fires at a threshold where the player is inside stone with a view out
of exactly one opening, so the plane's movement is **seen and not caught**. A
step the player's back is turned to is a bug, not a surprise.

### Who is doing this

In the world: it is the tide, and it has always done this. What is missing from
the coast is not the tide but the *announcement* of it — that is what Mercy was
for and what has been silent for fifty-one years.

On the rock, the hours are still counted, by one person. **Sister Ide's
hand-bell is the delve's clock**: each step is preceded by her ringing an hour
somewhere above or below the player, and she has been counting toward tonight's
Dead Ebb for fifty-one years. Her round is a countdown that nobody asked for and
nobody heard. Completing her rite (`OPT-B`) is the player asking, and its reward
is foreknowledge: **she tells the player what the sea will do next and what it
will uncover.** That is the classic shape — optional content buys you the tide
table, and the delve is completable without it.

At the very end the relation inverts once, and only once: the bell is rung and
the sea answers it. See *Endings*.

## What the tide changes, beat by beat

Honest accounting. Where a beat earns nothing from the tide, it is listed as
earning nothing and no mechanic is forced through it.

### Z0 · Barrow Shore — **transformed, twice**
- At `T-EBB1` the flat is walkable and the causeway to the mainland is dry: the
  road the answered walk at every low water, and the player has just walked it.
  The cairns stand clear. This is the delve's opening image and it only exists at
  an ebb.
- After `TIDE-1` the flat is sea. Z0 is closed for the middle of the delve, and
  raising the portcullis (`S1`) opens onto water — the shortcut's payoff is
  taken one beat *before* the step, deliberately, so it is not wasted.
- At `T-DEAD` the flat is bare and lower than living memory, and `S1` becomes a
  shortcut to somewhere new: below the old tide-stake line, on ground nobody has
  seen since before the Long Tide, **the rest of the answered are standing in
  the silt, facing the rock.** Optional, wordless, and the strongest image the
  delve has that is not the bell.

### Z1 · Cliff Road — **confirms a lesson, changes nothing else**
The main ledge is dry at every level. Only the `K2` gap — the section the player
has already been taught is gone — is reached by the flood, so a returning player
finds the sea filling the hole they once fell down. The tide **confirms** the
zone's lesson and never contradicts it. Nothing else here is touched, and
nothing else should be.

### Z2 · Gatehouse — **one image, one small change**
The channel down the passage floor is a dry gutter at the ebbs and brims to its
lip at the flood: the rock's drain becoming the rock's inlet, which is the whole
of Halgrave's fifty-one years in a two-block-wide detail. The murder-hole ambush
(`K3`) and the roof route are unaffected, and should be — the passage is the
delve's first taught arena and its geometry must stay fixed.

### Z3 · Drowned Ward — **transformed, and this is the mechanic's best beat**
- At `T-STAND` (first crossing) the causeway is dry and the ward is chest-deep:
  the zone as designed — spine safe, water optional, the wrecks (`OPT-C`) a
  genuine swim.
- After `TIDE-2` the causeway is awash and the ward is uncrossable at floor
  level. This is the moment `S3` earns its existence: the player opened the
  shortcut that means they never cross the ward again, and one hour later the
  ward cannot be crossed. **A shortcut that becomes the only route is worth more
  than a shortcut that saves a walk**, and the tide gives that for free.
- At `T-DEAD` the ward floor is dry: the arcades stand over a silt plain of
  weed, sunk boats and fifty-one years of dropped things, and the causeway is a
  wall through a field. `OPT-C`'s wrecks are a walk instead of a swim, which is
  a second window for a player who skipped them — and the pacifist route at the
  final boss is what that second window buys.

### Z4 · Chapel Ward — **earns one thing; it is not forced**
The ward is at `+9` and the sea never reaches it. The tide earns exactly one
beat here: the view out through the broken arcade at `TIDE-2`, the ward below
going under as the banded door opens. That is the whole of it. **The cloister
fight, Ide's round and the rite are unchanged, and should not be re-cut to
involve water.**

### Z5 · Hall & Keep — **earns nothing, and the absence is the point**
The hall is the highest, driest, most intact room on the rock and the sea has
never been in it. Ancel's household is the part of Halgrave that never got wet,
and the delve should say so by leaving this zone completely alone. The only
concession is `TIDE-3` firing on the descent stair as the player *leaves* — the
sea going out ahead of them, heard from a room the sea has never entered.

### Z6 · Cistern Deep — **the reason the mechanic exists**
- The player arrives at `T-STAND`: ankle-deep across the whole floor, exactly
  the concept image, with the well brimming and the supply channel (`K5`) black
  under the light shaft.
- The Founder is fought standing in that water, and he is comfortable in it.
- `TIDE-4` fires as he goes down: the water leaves, the well drains, and the
  bell's tongue is lying in silt that has not seen air since the year it was
  thrown there. **The delve's key item is not awarded and not unlocked — it is
  uncovered by the sea.**
- `K5`'s channel stays flooded at the Dead Ebb, so the zone's one lethal
  feature keeps its tell.

### Z7 · Bell Tower — **earns the endings and nothing else**
The tower is above every level. The climb, the broken flight and the stairhead
fight are unaffected by the tide and must not be re-cut around it. What the tide
gives Z7 is the view from the belfry — the whole rock at the lowest water in
fifty-one years, every zone the player has crossed visible and changed — and
the endings.

## Endings

Each ending is expressed by what the sea does. The bell says a number and the
water answers, which is the one moment in the delve when Halgrave's relationship
to its own bell inverts: for fifty-one years the bell reported the tide, and the
last hand makes the tide report the bell.

| ending | the sea |
|---|---|
| `END-THREE` | stays at `T-DEAD`. The causeway holds dry far past the hour it should, the answered walk off the rock, and the water does not come back until the last of them is across. |
| `END-TWO` | steps to `T-FLOOD` as the second note dies — the way is shut, and the sea makes it true. The answered turn on the stair. |
| `END-SILENT` | does not move. Ever again. The last image is the plane standing exactly where it is, at the lowest water in fifty-one years, with nothing to call it back. |

`END-THREE` is the only ending in which Hask makes the mainland, and the tide is
why his ask is precise rather than sentimental: he needs the causeway **dry**
and he needs it **empty**, and only three tolls at the Dead Ebb give him both —
the ebb clears the water and the toll clears the walkers.

## Anti-softlock

Machine-provable completability, checked against the schedule:

- The **rope** (`CP-05`) is taken on the cliff road before `TIDE-1`, and the
  ledge route passes *through* the rope store, so it cannot be walked past. If a
  build ever makes it optional, the store must be re-cut back onto the path.
- Z1's main ledge is dry at every level, so the cliff road is never closed and
  the rope is recoverable at any point in the run.
- Z0 is closed between `TIDE-1` and `TIDE-4` and holds nothing required.
- Z3 is uncrossable at floor level between `TIDE-2` and `TIDE-3`, and `S3` — the
  shortcut that makes it unnecessary — is opened by the same node that fires
  `TIDE-2`. The player cannot be on the wrong side of it.
- Z6 is enterable only at `T-STAND` and `T-DEAD`. The critical path enters it at
  `TIDE-3` and leaves at `TIDE-4`, both steps on the path itself.
- No optional strand is reachable in only one tide window, except `OPT-F`, which
  *is* a tide window — the Dead Ebb is the whole of it, and nothing depends on
  it. `OPT-C` has two windows; `OPT-A`, `OPT-B`, `OPT-D` and `OPT-E` are in
  zones the tide never closes.
