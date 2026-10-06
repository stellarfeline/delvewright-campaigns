# The Long Gallery

The demo level for **an endless corridor** (spec-0086) and **a loop's far field** (spec-0090). The level is one long straight hall with a light at its far end. Something stands up behind the party as they arrive, and they run for the light. The light never comes nearer until the hall has been run enough. There is no fog and no turn. The exit is in plain view the whole time, and the hall hides the jump only because the exit is far enough off that the jump moves it less on screen than you can see.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-long-gallery/

Its one piece, `prefab/long-gallery`, is in the prefab library (`prefabs/long-gallery.json` and four tiles, `long-gallery.x0y0z0.nbt` to `x0y0z3.nbt`). It is expanded from the grammar program `campaigns/the-long-gallery/design/programs/long-gallery.json` (5 × 5 × 172, seed 1, named in `zones.json` beside it).

## What it is

The hall is the eldritch spike's station 4, the one endless corridor walked on a client and judged seamless, rebuilt as a piece. Coordinates below are the piece's own; the hall runs south along z.

- **The den** (z 1–3): behind a glass wall at the back of the porch, lit from its roof. An armoured wither skeleton stands up in it as the party arrives.
- **The porch** (z 5–7): the party arrives here, facing south down the hall.
- **Twenty-six bays**, six courses each (z 8–163). Each bay has a lamp course, with a polished deepslate pillar in each wall and a soul lantern hung over the centre of the passage, then five open courses. A red carpet runs the length of the hall on a dark oak floor.
- **The slab** is the fifth course of the fourteenth bay (z 90), across the whole passage. Crossing it moves you 12 blocks back, two bays, with your facing and your speed kept. The loop counts its crossings in a party datum and holds while the count is at most 2. The third crossing is the last one it answers.
- **The exit** (z 164) is a doorway with a glowstone lintel, 74 blocks past the slab. It opens into a short room lit by two lanterns, where the bell stands (z 168). From the slab, the lintel's light is the brightest thing in view.

The approach behind the landing is 78 blocks deep, about as deep as the hall ahead of the slab. The rule judges every direction, and a player running from something looks back.

## What the engine proves, and how far off the exit has to be

Near the eye, out to 13.8 blocks for a 12-block jump, every visible block and every light level matches the bay it stands for. Past that, a cell may differ from what the slab sees, provided the jump moves it on screen by no more than 1.2852°. That number is not chosen: it is the largest shift in station 4's own view, which was walked and read as seamless. The build's loop binding states what it measured:

    loop binding: 1 loop(s); slab cells 9; eyes 24 (fog end 1024..1024 blocks as the kernel reads it); span 4200 cells closed in 95 steps, frontier cells closed by geometry 2010 and by fog 0, open faces 0; visible cells 3475 compared as blocks and as light at 2 skies over 1 configuration(s), 851 of them in the near field (13.8..13.8 blocks); far-field differences 396, largest shift 0.7374° of 1.2852°; volumes in span 0, bodies in the near field 0, bodies in the far field 1; forced route meets 1 of 1 holding, exercise steps 1

The 396 far differences are the exit, its light on the last courses, the room past it, and the porch and den behind. The largest shift any of them makes is 0.7374°. The figure in the den is the one body in the far field. A lit exit 56 blocks past the slab moves 1.467° and is refused (`refusals.md`).

## What to look for

Serve the level with the engine's playtest server (`tools/creator/playtest-server.sh up campaigns/the-long-gallery`), never in a singleplayer save. The staging gate refuses this build today; see *State*.

1. **At the spawn**, you hear something behind you, and the subtitle says *It stands up behind you. Run.* Turn round: something armoured stands behind the glass. Then look south. The hall runs straight to a lit doorway far off.
2. **Run for the light.** The bays come past, lamp after lamp. The doorway grows as you go.
3. **Cross the slab** (you will not see it). You are moved two bays back. You should feel no jolt and see no change: the same lamps, the same carpet, the doorway the same size it was a step ago. The subtitle reads *The light ahead is no nearer.*
4. **Keep running.** Cross it twice more: at a walk, at a sprint, and sprint-jumping. Each time the light stays where it was (*Two bays back. No nearer.*, then *Ahead, the light comes nearer.*).
5. **Look back as you cross**, once. Behind you is the long approach, the porch, and the glass. Nothing there should jump either.
6. **The fourth crossing** moves nobody. Run on to the doorway and into the lit room. Ring the bell; the delve completes.

What the engine does not check, by name: whether a client draws anything at the seam (it proves the move relative, the near field identical and the far field under the threshold); a body caught mid-jump, whose eye is higher than the one judged; particles and sounds alive at the move; items on the ground; what a second player sees; and chunk streaming at the far ring.

## The refusals

`refusals.md` holds the build's own words for three edits: the exit brought nearer, 56 blocks past the slab (`DW0947`, the worst far difference is the light on the floor before it); the approach cut to 36 blocks behind the landing (`DW0947`, read from the eye a walking body has when the slab catches it); and the approach cut to 18 (`DW0946`, the porch inside the near field).

## State

Builds on the engine's branch `feat/loop-far-end`. The machine ladder on the `validation/` image:

- **PackTest**: 22 of 22 required tests pass.
- **The mineflayer critical path** passes in 5 steps. It stands on the porch, walks to the slab, crosses it three times and reads each move as exactly `[0, 0, -12]`, then walks on and rings the bell.

The staging gate refuses this build with 2 reds, drill3-01 and drill3-03. Both concern the design record, which a demo level does not carry. Serving the build takes the gate's own deliberate override, which this branch has not used.
