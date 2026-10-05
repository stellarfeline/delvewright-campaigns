# The Beached Thing

The demo level for **a body the size of a hill** (spec-0087): a prefab sculpted
by `delvec sculpt` from a declared form, lying on its own ground, walked inside
and onto its back by the proofs the engine already has.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-beached-thing/

Its one piece is sculpted from a committed form, which is the artifact of
record; the structure parts beside it are what the form sculpts to:

    demos/the-beached-thing/forms/the-beached-thing.json   # the form
    demos/the-beached-thing/prefabs/                        # its output, regenerated, never edited

Regenerate the piece (the same form and seed always write the same bytes):

    rm -rf demos/the-beached-thing/prefabs
    delvec sculpt demos/the-beached-thing/forms/the-beached-thing.json -o demos/the-beached-thing/prefabs

## What it is

A stranded creature, 146 blocks from snout to flukes, sunk to its belly in a
mud flat on a valley floor (the piece's box is 62 × 60 × 146; the body rises to
45 blocks at the shoulder). The ground is part of the piece: a five-course
apron of packed mud fills its whole footprint, and the lower flanks are a wall
you cannot walk up.

Its parts, as the form declares them:

- **The head** lies on the mud at the north-west corner, snout to the north,
  jaw dropped, with an eye socket and the gape of the mouth cut into it. A
  short neck leaves the front of the shoulder below its crest and turns west
  to it.
- **The shoulder** is the highest point of the back; behind it the torso
  narrows to the hips and the back falls away to the south.
- **The tail** bends east and sweeps back west for about sixty blocks, ending
  in two flukes laid flat on the mud. A split across its root, behind the
  hips, keeps it from being a ramp onto the back.
- **Two flippers** lie splayed on the mud, one on each flank.
- **The spine** shows as a row of vertebral spines along the back, and **rib
  bands** stand out of both flanks behind the wound.
- **The wound** is on the west flank over bay A: the hide is torn away over a
  red-brown hollow, four ribs arch out of it and down onto the mud, and two
  broken ones hang over the way in.

The tones come from the sculpt's own shading, which puts each block on one of
four tiers by its surface normal and openness: bone (bone block, calcite) on
the thin and upward-facing parts, which is where the spines, ribs, skull,
flippers and flukes are; dark leathery hide (cyan, light gray, gray, black and
brown terracotta) on the back and flanks; red-brown flesh (red, brown and pink
terracotta, nether wart block) in the crevices, the wound and the two bays. No
stone block is in the body.

World coordinates below are the built ones (the piece's origin is 0, 59, 0;
the mud is walked at y 64).

- **You arrive** on the mud on the west side (1, 64, 50), facing the wound.
  The way in is a cut four blocks high through the hollow at grade
  (z 53–57), between the broken ribs.
- **Bay A, soul lanterns** — the first room inside, centred at (31, 64, 55),
  about 26 wide and 28 long, floored by the mud. Twelve soul lanterns stand on
  its floor, two more in the wound and one at the mouth of the passage.
- **The passage** runs south from bay A to bay B (x 29–33, z 66–81), with one
  soul lantern (z 73) and one crying obsidian block (z 76) at its middle.
- **Bay B, crying obsidian** — the second room, centred at (31, 64, 90), about
  22 wide and 24 long. Eleven crying obsidian blocks stand on its floor.
- **The way up** is a stair cut along the east flank: it starts on the mud
  east of the hips (45, 64, 112), climbs north along the flank's own contour,
  its outer side open to the sky, and ends on the back at the shoulder
  (31, 104, 38). It is the only way onto the body.
- **The back**: the top of the body, open to the sky, from the shoulder south
  along the spine.

Both bays are lit only by the lights placed in the form; neither has a cut to
the sky. The two light blocks emit the same level (10) and stand on a similar
grid, about six blocks apart, so the two rooms differ mainly in the block that
gives the light.

## How the body is made to read

Researched, not invented; each rule below says which.

- **The silhouette carries the reading** (cited). A form that reads at a
  distance is one recognisable from its outline alone, built as a hierarchy of
  large, medium and small shapes ([World of Level Design, *Silhouette Design
  for Game Environments*][wold]). Here the large shape is the torso; the
  medium shapes that break its outline are the head and neck, the tail and
  flukes, and the flippers; the small ones are the spines and ribs.
- **Skull, jaw, vertebrae and ribs are what a large carcass shows** (cited).
  A stranded minke whale observed for two years turned grey, then white and
  brown in patches, then reddish-brown and dark brown, its skin drying like
  leather; rib contours showed through it at seven months, and its jawbones
  and most vertebrae were bare by eighteen ([Baptist et al., *Decomposition of
  a minke whale carcass in a temperate dune ecosystem*, Frontiers in Marine
  Science, 2025][minke]). Hence dark leathery hide with pale patches, white
  spines, rib bands and a white skull.
- **A walkable carcass is flesh, bone and earth** (cited). Monster Hunter:
  World's Rotten Vale is a valley formed by the remains of a giant serpent,
  its caverns "decorated with pale earth, tan rotting flesh, and bloody
  remains" ([Monster Hunter Wiki, *Rotten Vale*][vale]). Hence red-brown flesh
  inside the body and in the wound.
- **No stone texture on the body** (authored): a pale stone-and-coral palette
  on this form read as a boulder from afar and a cliff from the ground, so
  every tone is terracotta, bone or nether wart.

[wold]: https://www.worldofleveldesign.com/categories/game_environments_design/silhouette-design-game-environments.php
[minke]: https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2025.1474460/full
[vale]: https://monsterhunterwiki.org/wiki/Rotten_Vale

## What to look for

1. **At the spawn**, look along the body, then turn north to the head: does it
   read as one stranded animal at this scale, with a head, a back and a tail?
2. **Look at the wound** before you walk in: do the ribs read as ribs, and the
   hollow as torn flesh rather than a cave mouth?
3. **Walk in** to bay A. Stand in the middle and look round: does the
   soul-lantern light read as the body's own light, or as lanterns set down in
   a cave?
4. **Walk south through the passage** into bay B and do the same with the
   crying obsidian. Compare the two rooms: which one belongs to the inside of a
   body? This is the open craft question the level exists to answer.
5. **Go back out**, walk round to the stair on the east flank by the hips and
   climb it. Does the stair read as cut into the body?
6. **Walk the back** from the shoulder along the spines, and look down from
   the edge: the fall to the mud is one you can see coming.

## State

Builds on the engine's integration branch `integration/stranding-capabilities`
(revision 9923c1bb). The quest walks the spawn, bay A, bay B and the back in
order; the build proves the route (`DW0311`: 3 legs walked), finds no place a
body can get into and not out of (`DW0921`: 0 of 16532 reachable cells), and
measures every walkable cell lit (`DW0210`). `delvec sculpt` itself reports
`pockets: 0 place(s)` of 10618 reachable cells and all four standing anchors
reached from grade.

Serve it with the engine's playtest server:

    tools/creator/playtest-server.sh up campaigns/the-beached-thing --prefabs demos/the-beached-thing/prefabs

It is never copied into a singleplayer save.

The machine ladder on the `validation/` image: PackTest passed (16 of 16
required tests), and the mineflayer critical path passed (5 steps: spawn,
bay A, bay B, the back; its die-retry and death-loop stages did not run,
because the level declares no combat and no death plan).
The staging gate, against the findings ledger at engine revision 1cd6cd1f,
refuses it with 2 reds, both about the design record a demo level does not
yet carry: drill3-01 and drill3-03. Serving it to a person takes the gate's
own deliberate override, which is the owner's call.
