# The Long Gallery

The demo level for **an endless corridor** (spec-0086): `loops[]`, a slab across a corridor that sends every body crossing it one bay back, until the party has walked it enough. It also shows the one way a **straight** corridor can loop: an atmosphere (spec-0080) whose fog closes the view before the far end or the seam can be seen.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-long-gallery/

Its one piece, `prefab/long-gallery`, is in the prefab library (`prefabs/long-gallery.{nbt,json}`). It is expanded from the grammar program `campaigns/the-long-gallery/design/programs/long-gallery.json` (37 × 5 × 43, seed 1, named in `zones.json` beside it).

## What it is

A straight stone-brick gallery, three cells wide and three tall, walled at both ends and floored in smooth stone. Every bay mouth is framed by a rib of polished deepslate: a pier in each wall and a band across the roof. The gallery stands in empty space, 16 cells clear on each side and 8 at each end. That margin is part of the piece because an area's sky is painted over its piece's bounds, and the client blends fog from about 12 blocks round the eye. Without the margin, the fog an eye reads is thinned by the unpainted air outside. Coordinates below are the piece's own; the passage runs along x 17–19 and south along z.

- **The air** is `atmosphere/close-air`, carried by the gallery's area from the first tick. It is a near-black fog (`#16130f`) that begins 2 blocks from the eye and is solid at 8. Inside the gallery you see the bay you are in and the next rib, then the dark. You never see the far end.
- **The porch** (z 9–11): you arrive here, facing south down the gallery.
- **Three identical bays**, six courses each (z 12–29). Each bay is its ribbed mouth, a lantern hung from the roof over the middle of the passage, and four open courses.
- **The slab** is the mouth of the third bay (z 24), across the whole passage. Crossing it moves you six blocks back, to the mouth of the second bay (z 18), and keeps your facing and your speed. What you see there is what you saw before you crossed, block for block and light for light, as far as the fog lets you see. The engine refuses to build the level otherwise.
- **The release**: the loop counts its crossings in a party datum and holds while the count is at most 2. The third crossing is the last one it answers; after that the slab is ordinary floor.
- **The end room** (z 30–33) opens like a fourth bay's mouth, rib and all, with its lantern where that bay's would hang. The bell stands at its far end (z 33) from the world's first tick. A one-cell `world-edits.json` batch sets it at setup, and the quest's `interact` objective names the same block as its prop, so its activation writes what is already there.

## What to look for

Serve the level with the engine's playtest server (`tools/creator/playtest-server.sh up campaigns/the-long-gallery`), never in a singleplayer save. The staging gate refuses this build today; see *State*.

1. **At the spawn**, look south down the gallery. You see the porch, the first rib and its lantern, and then dark air. Nothing reads as an end. Press F3: the biome is `the-long-gallery:atmosphere/close-air`.
2. **Walk south through the first two bays.** Each rib and lantern comes out of the dark as you walk towards it. Nothing happens. The fog should look like dimness, not like coloured smoke.
3. **Cross the mouth of the third bay.** You are moved six blocks back. You should not feel a jolt, a turn or a change of speed. Nothing in front of you changes: the same rib, the same lantern, the same light on the walls, the same dark beyond. The subtitle reads *The lamp ahead is lit, as it was.*
4. **Cross it twice more**: at a walk, at a sprint, and sprint-jumping. Each crossing moves you back the same way (*Another bay. The same bay.*, then *Ahead, the way is open.*).
5. **Cross it a fourth time.** Nothing moves you. Walk on: the end room's rib and the bell come out of the dark. Ring the bell; the delve completes.
6. **With a second player**: stand still in the second bay and watch the first player cross the slab. You see them walk into the dark ahead and come up behind you. The engine does not hide this. A loop is one body's experience, and a party that wants it seamless walks it one at a time.

What the engine does not check, by name: whether a client draws anything at the seam (it proves the move relative, and the view identical up to the fog end), how the fog itself looks, particles and sounds alive at the move, items on the ground, what a second player sees, and chunk streaming at the far ring.

## The refusals

`refusals.md` holds the build's own words for six edits. **The fog removed** is `DW0948`: the whole hall comes into view, so the span grows to both end walls and takes in the bell. **The fog thinned** from 8 to 8.3 blocks is `DW0946`: the eye on the slab sees the bell, and the same spot seen from the landing is empty air. **The paint cut to the gallery** (the piece without its margin) is `DW0948` again: the fog an eye reads is thinned, and the span grows to the walls. Then three refusals that do not involve the fog: a lantern missing from the landing bay, a lamp hidden in the fog that lights one section brighter than its image (both `DW0946`), and a slab one course thick under a fall (`DW0945`).

## State

Builds on the engine's integration branch `integration/stranding-capabilities` (revision edab67d9). The build's loop line:

    loop binding: 1 loop(s); slab cells 9; eyes 15 (fog end 8..8 blocks as the kernel reads it); span 475 cells grown to a closed view in 10 steps, boundary cells closed by geometry 304 and by fog 18, open faces 0; visible cells 329 compared as blocks and as light at 2 skies over 1 configuration(s); volumes in span 0, bodies in span 0; forced route meets 1 of 1 holding, exercise steps 1

The machine ladder on the `validation/` image:

- **PackTest**: 18 of 18 required tests pass. Among them are `loop_the_gallery` (a body in the slab is moved by exactly the offset and the count rises by one), `loop_the_gallery_released` (with the count past the release, the same poll moves nothing) and `atmosphere_places` (after the setup paint, a cell in the gallery stands in `atmosphere/close-air` and a cell above the paint does not).
- **The mineflayer critical path** passes in 4 steps. It walks to the slab, crosses it three times and reads each move as exactly `[0, 0, -6]`, then walks on and rings the bell.

The staging gate, against the findings ledger at engine revision 1cd6cd1f, refuses this build with 2 reds, drill3-01 and drill3-03. Both concern the design record, which a demo level does not yet carry. Serving the build takes the gate's own deliberate override, which this branch has not used.
