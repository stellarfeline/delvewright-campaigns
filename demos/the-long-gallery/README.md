# The Long Gallery

The demo level for **an endless corridor** (spec-0086): `loops[]`, a slab across a corridor that returns every body crossing it one bay back, until the party has walked it enough.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-long-gallery/

Its one piece, `prefab/long-gallery`, is in the prefab library (`prefabs/long-gallery.{nbt,json}`) and is expanded from the grammar program `campaigns/the-long-gallery/design/programs/long-gallery.json` (5 × 5 × 27, seed 1, named in `zones.json` beside it).

## What it is

A stone-brick gallery three cells wide and three tall, closed at both ends, floored in smooth stone. Every bay mouth is framed by a rib of polished deepslate, a pier in each wall and a band across the roof, so the gallery reads as a run of bays rather than a tunnel.

- **The porch** (z 1–3): you arrive here, facing south down the gallery.
- **Three identical bays**, six courses each (z 4–21). Every bay is the same: its ribbed mouth, a lantern hung from the roof over the middle of the passage, a baffle across the two western cells, two open courses, and a baffle across the two eastern cells. The baffles stagger, so you walk a zigzag and your view down the gallery closes inside one bay.
- **The slab** is the mouth of the third bay (z 16), the whole cross-section of the passage. Crossing it moves you six blocks back, to the mouth of the second bay (z 10), with your facing and your speed kept. What you see there is what you saw before you crossed, block for block and light for light; the engine refuses to build the level otherwise.
- **The release**: the loop counts its crossings in a party datum and holds while the count is at most 2. The third crossing is the last one it answers; after it the slab is ordinary floor.
- **The end room** (z 22–25) opens like a fourth bay's mouth, rib and all, with its lantern where that bay's would hang. The bell is at its far end.

## What to look for

Serve the level with the engine's playtest server (`tools/creator/playtest-server.sh up campaigns/the-long-gallery`), never in a singleplayer save. The staging gate refuses this build today; see *State*.

1. **At the spawn**, look down the gallery: a lantern, a baffle on your right, then one on your left. You cannot see the far end.
2. **Walk south through the first two bays.** Zigzag round the baffles. Nothing happens.
3. **Cross the mouth of the third bay.** You are moved six blocks back. You should not feel a jolt, a turn or a change of speed, and nothing in front of you changes: the same lantern, the same baffles, the same light on the walls. The subtitle reads *The lamp ahead is lit, as it was.*
4. **Cross it twice more**, at a walk, at a sprint, and sprint-jumping. Each crossing moves you back the same way (*Another bay. The same bay.*, then *Ahead, the way is open.*).
5. **Cross it a fourth time.** Nothing moves you. Walk on into the end room and ring the bell; the delve completes.
6. **With a second player**: stand still in the second bay and watch the first cross the slab. You see them vanish at the slab and reappear behind you. The engine does not hide this; a loop is one body's experience, and a party that wants it seamless walks it one at a time.

What the engine does not check, by name: whether a client draws anything at the seam (it proves the move relative and the view identical), particles and sounds alive at the move, items on the ground, what a second player sees, and chunk streaming at the far ring.

## The refusals

`refusals.md` holds the build's own words for four edits: the baffles removed, the lantern missing from the bay you land in, a lamp round the corner that lights one bay brighter, and a slab one course thick under a fall.

## State

Builds on the engine branch `feat/seamless-loop`. The machine ladder on the `validation/` image:

- **PackTest**: 17 of 17 required tests pass, among them `loop_the_gallery` (a body in the slab is moved by exactly the offset and the count rises by one) and `loop_the_gallery_released` (with the count past the release, the same poll moves nothing). Each goes red alone when its half of the emission is removed: with the move's `tp` line deleted, `loop_the_gallery` fails (*expected -6000, got 0*); with the poll's gate deleted, `loop_the_gallery_released` fails (*expected 0, got 1*).
- **The mineflayer critical path** passes in 4 steps: it walks to the slab, crosses it three times and reads each move as exactly `[0, 0, -6]`, then walks on and rings the bell.

The staging gate refuses this build with six findings about objects a demo level does not author (an item-gated interaction and a cast: isl-02, isl-35, isl-41, isl-46; a design record: drill3-01, drill3-03), the same six it reports on The Threshold. Serving it takes the gate's own deliberate override, which this branch has not used.
