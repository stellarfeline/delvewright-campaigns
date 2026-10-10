# The Listening Hall — design record

The demo level for the sculk family (spec-0100): sensors, shriekers and a catalyst admitted by state, at rest, a sensor's power reaching nothing, a catalyst where no body can die, and the walk's vibrations asserted by the bot. Ten minutes, one player, no NPCs, no fight.

## Layout

A sealed site cut out of deepslate, three rooms in a line from south to north, one floor (y 64), each detailed from its own program (`programs/`, written by `design/programs-src/rooms.py` from the place handouts): deepslate-tile floors, deepslate-brick walls and ceilings.

| place | box (x, z) | what it is |
| --- | --- | --- |
| `node/antechamber` | 8201–8207, 8236–8242 | where the party arrives; a quiet floor out of every sensor's hearing |
| `node/hall` | 8200–8208, 8210–8234 | the listening hall, 9 × 25, four blocks of headroom, chiseled pilasters every four blocks down both long walls |
| `node/far-door` | 8202–8206, 8204–8208 | an alcove past the north arch; the way out |

The hall:

- **Sensors in the floor.** Six plain `sculk_sensor`s set into the floor course along both walls (x 8200 and x 8208), staggered, so wherever a body walks down the middle it is inside the hearing of at least one, and every footstep clicks.
- **The shrieker in the dark.** A `sculk_shrieker[can_summon=false]` in a niche in the west wall at walk height, within eight blocks of the nearest sensors. It answers every click a player's step sets off with its sound and its particles and nothing else: no warning, no darkness, no warden.
- **The calibrated sensor at the far door.** A `calibrated_sculk_sensor[facing=north]` set in the alcove's north wall at walk height, so its input side is the alcove's open air and it hears every frequency, from sixteen blocks.
- **The light.** Thirteen soul lanterns hang from the hall ceiling in two staggered rows, so its darkest walkable cells (along the walls between lanterns) sit at light 3: dim and blue. The antechamber and the alcove each hang one ordinary lantern, warm and brighter, so the hall reads as the dark between them.
- **The glass well.** A 3 × 3 glass lid in the floor at the hall's centre over a shaft; a `sculk_catalyst` glows at its bottom, ten blocks under the lid, farther than any body can be from it.

## Beats

1. **Arrive** in the antechamber (campaign start).
2. **Walk the hall to the well** (`obj/stand-over-the-well`, reach the centre of the hall). Every step clicks a sensor; the shrieker answers. A chat line on the glass: something glows far down and does not move.
3. **Go out by the far door** (`obj/reach-the-far-door`). Walking north, the calibrated sensor in the alcove's wall clicks.
4. **The bloom.** Reaching the alcove fires the floor's one story beat: the hall floor between the two rows of sensors is overgrown with sculk — one `fill-region` of `minecraft:sculk_vein[down=true]` over the walk plane (hall centre ± [3, 0, 10]), never over a sensor — `sculk_charge_pop` and `sculk_soul` puff over it, and `block.sculk_catalyst.bloom` plays from the well. The campaign completes 200 ticks later.

No branch points, one ending.

## Departures from the demo row

Both are forced by the engine and recorded as toolchain findings:

- The row's `fill-region` of `minecraft:sculk` cannot reach the floor course: a `fill-region` box is centred on an anchor, and every anchor stands on the walk plane, so a box that holds the floor course holds the walk plane above it too. The floor is overgrown with veins at walk height instead.
- The bloom fires at the far door rather than at the well: the engine models a `fill-region` of any non-fluid block, a vein included, as solid, so a bloom with a leg still to walk is proved as a raised floor the party is trapped behind (`DW0921`). At the far door no leg follows it.
