# The Long Gallery

The demo level for **an endless corridor** (spec-0086): `loops[]`, a slab across a corridor that sends every body crossing it one bay back, until the party has walked it enough. It also shows the one way a **straight** corridor can loop: an atmosphere (spec-0080) whose fog closes the view before the far end or the seam can be seen. The far end is an unlit room, so a body that does reach it walks into the dark.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-long-gallery/

Its one piece, `prefab/long-gallery`, is in the prefab library (`prefabs/long-gallery.{nbt,json}`). It is expanded from the grammar program `campaigns/the-long-gallery/design/programs/long-gallery.json` (37 × 5 × 45, seed 1, named in `zones.json` beside it).

## What it is

A straight stone-brick gallery, three cells wide and three tall, walled at both ends and floored in smooth stone. Every bay mouth is framed by a rib of polished deepslate: a pier in each wall and a band across the roof. The gallery stands in empty space, 16 cells clear on each side. That margin is part of the piece because an area's sky is painted over its piece's bounds, and the client blends fog from about 12 blocks round the eye. Without the margin, the fog an eye reads is thinned by the unpainted air beside it. Coordinates below are the piece's own; the passage runs along x 17–19 and south along z.

- **The air** is `atmosphere/close-air`, carried by the gallery's area from the first tick. It is a near-black fog (`#16130f`) that begins 2 blocks from the eye and is solid at 14.2. You see about two bays ahead, fading into dark. 14.2 is the largest fog end the engine accepts for this gallery, to a tenth of a block. The gallery is as long as it is so the fog can be that thin: one bay before the bays the loop repeats, and two after the slab.
- **The porch** (z 1–3): you arrive here, facing south down the gallery.
- **Six identical bays**, six courses each (z 4–39). Each bay is its ribbed mouth, a lantern hung from the roof over the middle of the passage, and four open courses.
- **The slab** is the mouth of the fourth bay (z 22), across the whole passage. Crossing it moves you six blocks back, to the mouth of the third bay (z 16), and keeps your facing and your speed. What you see there is what you saw before you crossed, block for block and light for light, as far as the fog lets you see. The engine refuses to build the level otherwise.
- **The release**: the loop counts its crossings in a party datum and holds while the count is at most 2. The third crossing is the last one it answers; after that the slab is ordinary floor.
- **The end room** (z 40–43) opens like a seventh bay's mouth, rib and all, but it has no lamp. Its only light spills in from the last bay's lantern. By hand from the block-light rule (not measured), that is about 7 at its mouth and 4–5 at the bell. The engine's darkness rule, `DW0210`, refuses a reachable floor cell below 3, and it does not fire. The bell stands at the room's far end (z 43) from the world's first tick. A one-cell `world-edits.json` batch sets it at setup, and the quest's `interact` objective names the same block as its prop, so its activation writes what is already there.

The darkness does not close the view for the engine. `DW0947` counts only walls and fog, because how dark a dark room looks depends on the player's brightness setting. Darkness also does not let the fog thin: the loop compares light through the seam, so an unlit room just past the slab's bay makes the fog thicker, not thinner (see *The refusals*).

## What to look for

Serve the level with the engine's playtest server (`tools/creator/playtest-server.sh up campaigns/the-long-gallery`), never in a singleplayer save. The staging gate refuses this build today; see *State*.

1. **At the spawn**, look south down the gallery. You see two or three ribs and their lanterns, each fainter than the last, and then dark air. Nothing reads as an end. Press F3: the biome is `the-long-gallery:atmosphere/close-air`. The gallery should look dim, not smoky.
2. **Walk south through the first three bays.** Each rib and lantern comes out of the dark as you walk towards it. Nothing happens.
3. **Cross the mouth of the fourth bay.** You are moved six blocks back. You should not feel a jolt, a turn or a change of speed. Nothing in front of you changes: the same ribs, the same lanterns, the same light on the walls, the same dark beyond. The subtitle reads *The lamp ahead is lit, as it was.*
4. **Cross it twice more**: at a walk, at a sprint, and sprint-jumping. Each crossing moves you back the same way (*Another bay. The same bay.*, then *Ahead, the way is open.*).
5. **Cross it a fourth time.** Nothing moves you. Walk on through two more bays. Past the last lantern, the gallery opens into a room with no lamp. Walk in: the bell should be plain to see and to ring in the spill from behind you. Ring it; the delve completes.
6. **With a second player**: stand still in the third bay and watch the first player cross the slab. You see them walk into the dark ahead and come up behind you. The engine does not hide this. A loop is one body's experience, and a party that wants it seamless walks it one at a time.

What the engine does not check, by name: whether a client draws anything at the seam (it proves the move relative, and the view identical up to the fog end), how the fog and the dark room look, particles and sounds alive at the move, items on the ground, what a second player sees, and chunk streaming at the far ring.

## The refusals

`refusals.md` holds the build's own words for seven edits:

- **The fog removed** is `DW0948`. The whole hall comes into view, so the span grows to both end walls and takes in the bell. The unlit room does not stop it.
- **The fog thinned** from 14.2 to 14.3 blocks is `DW0946`. The eye on the landing reaches the back of the porch, which is lit differently from its image in the bays.
- **The two bays after the slab removed** is `DW0948`. The unlit end room is then within the fog's reach from the slab.
- **The paint cut to the gallery** (the piece without its side margin) is `DW0948`.
- Three edits that do not involve the fog: a lantern missing from the landing bay and a lamp hidden in the fog that lights one section brighter than its image (both `DW0946`), and a slab one course thick under a fall (`DW0945`).

## State

Builds on the engine's integration branch `integration/stranding-capabilities` (revision edab67d9). The build's loop line:

    loop binding: 1 loop(s); slab cells 9; eyes 15 (fog end 14.2..14.2 blocks as the kernel reads it); span 775 cells grown to a closed view in 16 steps, boundary cells closed by geometry 496 and by fog 18, open faces 0; visible cells 579 compared as blocks and as light at 2 skies over 1 configuration(s); volumes in span 0, bodies in span 0; forced route meets 1 of 1 holding, exercise steps 1

The machine ladder on the `validation/` image:

- **PackTest**: 18 of 18 required tests pass. Among them are `loop_the_gallery` (a body in the slab is moved by exactly the offset and the count rises by one), `loop_the_gallery_released` (with the count past the release, the same poll moves nothing) and `atmosphere_places` (after the setup paint, a cell in the gallery stands in `atmosphere/close-air` and a cell above the paint does not).
- **The mineflayer critical path** passes in 4 steps. It walks to the slab, crosses it three times and reads each move as exactly `[0, 0, -6]`, then walks on and rings the bell.

The staging gate, against the findings ledger at engine revision 1cd6cd1f, refuses this build with 2 reds, drill3-01 and drill3-03. Both concern the design record, which a demo level does not yet carry. Serving the build takes the gate's own deliberate override, which this branch has not used.
