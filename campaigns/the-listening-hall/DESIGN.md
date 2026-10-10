# The Listening Hall — design record

The demo level for the sculk family (spec-0100): sensors, shriekers and a catalyst admitted by state, at rest, a sensor's power reaching nothing, a catalyst where no body can die, and the walk's vibrations asserted by the bot. Ten minutes, one player, no NPCs, no fight.

## Layout

A sealed site cut out of deepslate, three rooms in a line from south to north, one floor (y 64):

| place | box (x, z) | what it is |
| --- | --- | --- |
| `node/antechamber` | 8201–8207, 8236–8242 | where the party arrives; a quiet floor out of every sensor's hearing |
| `node/hall` | 8200–8208, 8210–8234 | the listening hall, 9 × 25, six blocks of headroom |
| `node/far-door` | 8202–8206, 8204–8208 | an alcove past the north arch; the way out |

The hall:

- **Sensors in the floor.** Plain `sculk_sensor`s set into the floor course along both walls (x 8200 and x 8208), staggered, so wherever a body walks down the middle it is inside the hearing of at least one, and every footstep clicks.
- **The shrieker in the dark.** A `sculk_shrieker[can_summon=false]` in a niche in the west wall at walk height, within eight blocks of the nearest sensors. It answers every click a player's step sets off with its sound and its particles and nothing else: no warning, no darkness, no warden.
- **The calibrated sensor at the far door.** A `calibrated_sculk_sensor` set in the alcove's north wall at walk height, facing into the alcove, so its input side is the alcove's open air and it hears every frequency, from sixteen blocks.
- **The glass well.** A 3 × 3 glass lid in the floor at the hall's centre over a shaft; a `sculk_catalyst` glows at its bottom, ten blocks under the lid, farther than any body can be from it.

## Beats

1. **Arrive** in the antechamber (campaign start). A line says the hall beyond is sealed and listening.
2. **Walk the hall to the well** (`obj/stand-over-the-well`, reach the centre of the hall). Every step clicks a sensor; the shrieker answers.
3. **The bloom.** Standing on the lid fires the floor's one story beat: the hall's floor between the two rows of sensors turns to `minecraft:sculk` (four `fill-region`s around the lid, never over a sensor), `sculk_charge_pop` and `sculk_soul` puff over it, and `block.sculk_catalyst.bloom` plays from the well.
4. **Go out by the far door** (`obj/reach-the-far-door`). Walking north, the calibrated sensor in the alcove's wall clicks; reaching the alcove completes the delve.

No branch points, one ending.
