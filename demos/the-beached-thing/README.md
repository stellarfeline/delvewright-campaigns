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
mud flat on a valley floor, with a bank of mud standing off its west flank to
look at it from. The piece's box is 148 × 60 × 146: the body fills its east
62 blocks and rises to 45 at the shoulder, and the ground is part of the piece
— a five-course apron of packed mud fills the whole footprint, and the lower
flanks are a wall you cannot walk up.

Its parts, as the form declares them:

- **The head** lies on the mud at the north-west corner of the body, snout to
  the north, jaw dropped, with an eye socket and the gape of the mouth cut into
  it. A short neck leaves the front of the shoulder below its crest and turns
  west to it.
- **The shoulder** is the highest point of the back; behind it the torso
  narrows to the hips and the back falls away to the south.
- **The tail** leaves the body from under the rump, below the hips' widest
  line, bends east and sweeps back west for about sixty blocks, ending in two
  flukes laid flat on the mud. The rump stands over its root as a wall several
  blocks high, so the tail is not a ramp onto the back.
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
terracotta, nether wart block) in the crevices, the wound and the bays. No
stone block is in the body. The mud bank is its own material (packed mud,
coarse and rooted dirt, mud-brick steps), so it reads as ground, not as part of
the animal.

World coordinates below are the built ones (the piece's origin is 0, 59, 0;
the mud is walked at y 64).

- **You arrive** on the mud between the bank and the body (36, 64, 64), facing
  the body.
- **The vantage** — a bank of mud on the valley floor west of the body, with a
  worn path up its east side to a flat top at (16, 69, 71). From there the whole
  body is in front of you: it spans 91 degrees of the horizon (Minecraft's
  default field of view shows about 102 at 16:9) and 24 degrees of height, from
  70 to 132 blocks away — inside the served view distance of 10 chunks (its
  farthest block is 8 chunks off).
- **The wound and the way in** — a cut through the hollow at grade
  (x 85–108, z 52–56), between the broken ribs.
- **Bay A, soul lanterns** — the first room inside, centred at (117, 64, 55),
  19 wide and 28 long. A mass of flesh stands in its middle from floor to vault,
  so the floor is a ring about four blocks wide round it.
- **The passage** runs south from bay A to bay B (x 115–118, z 66–80), three
  blocks high.
- **Bay B, crying obsidian** — the second room, centred at (117, 64, 90), 18
  wide and 24 long, with two columns of flesh standing in it.
- **The east door** leaves bay B at grade (x 119–138, z 99–103) and passes
  under the stair out onto the mud of the east flank.
- **The way up** is a stair cut along the east flank: it starts on the mud
  east of the hips (131, 64, 112), climbs north along the flank's own contour,
  its outer side open to the sky, and ends on the back at the shoulder
  (117, 104, 38). It is the only way onto the body: sculpted without it, the
  walk from grade does not reach the back.
- **The back**: the top of the body, open to the sky, from the shoulder south
  along the spine.

### The light inside

No lantern stands on a floor. Every source inside is set into the body's own
surface by the sculpt (`lights[].hull`, spec-0087 §9), drawn as a seeded
Poisson-disk scatter — staggered and irregular, never a grid — over walls and
vault:

- **Bay A**: soul lanterns, **recessed** — each sits one block behind the
  surface, hidden behind a polished-granite stair set in the surface, with a
  one-block slot beside the stair through which its light comes out. A dense
  band at floor height (34 sources, spacing 2.75) lights the floor; a second
  entry over walls and vault (41 sources, 12 of them in the vault, spacing 3)
  lights the upper space. The light reaches the room at level 7 in front of
  each slot.
- **Bay B**: crying obsidian, **embedded** — flush in the surface, a block of
  the wall or vault itself (55 sources, 37 wall and 18 vault, spacing 3.5).
- **The passage** (5 sources) and **the mouth of the wound** (13 sources):
  soul lanterns, recessed, as in bay A.

So the two rooms now differ in kind as well as in block: bay A is lit by
hidden lanterns, bay B by a glowing body. The research behind these rules and
their numbers is in the engine's `docs/reference/interior-lighting.md` §7.

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

1. **Go to the vantage first.** Turn round from where you arrive, take the worn
   path up the mud bank, and stand on its top facing east: does the whole thing
   read as one stranded animal at this distance, with a head, a back and a tail?
2. **Look at the wound** as you walk to it: do the ribs read as ribs, and the
   hollow as torn flesh rather than a cave mouth?
3. **Walk in** to bay A. Stand in the ring and look round and up: does the
   light read as the body's own, coming out of the walls and the vault, or as
   lanterns someone put there? Is the upper space lit, and does the slot of a
   hidden lantern read as part of the wall?
4. **Walk south through the passage** into bay B and do the same with the
   crying obsidian set into the walls and vault. Compare the two rooms: which
   one belongs to the inside of a body? This is the open craft question the
   level exists to answer.
5. **Go out through the east door**, under the stair, turn south to its foot
   by the hips and climb it. Does the stair read as cut into the body? On the
   way, look at where the tail leaves the body: the rump should stand over it,
   with no gap across its root.
6. **Walk the back** from the shoulder along the spines, and look down from
   the edge: the fall to the mud is one you can see coming.

## State

Builds on the engine's `feat/organic-giant` branch (revision 3677b4f4; the
hull light is spec-0087 §9 there). The quest walks the vantage, bay A, bay B
and the back in order; the build proves the route (4 legs walked), finds no
place a body can get into and not out of (`DW0921`: 0 of 31154 reachable
cells), and measures every walkable cell lit (`DW0210` silent). `delvec
sculpt` itself reports `pockets: 0 place(s)` of 22763 reachable cells and all
five standing anchors reached from grade; sculpted twice, the bytes are
identical.

Serve it with the engine's playtest server:

    tools/creator/playtest-server.sh up campaigns/the-beached-thing --prefabs demos/the-beached-thing/prefabs

It is never copied into a singleplayer save.

The machine ladder on the `validation/` image: PackTest passed (17 of 17
required tests), and the mineflayer critical path passed (6 steps: spawn, the
vantage, bay A, bay B, the back; its die-retry and death-loop stages did not
run, because the level declares no combat and no death plan).
The staging gate, against the findings ledger at engine revision 1cd6cd1f,
refuses it with 2 reds, both about the design record a demo level does not
yet carry: drill3-01 and drill3-03 (14 bound, 81 inapplicable, 25 declared
uncoverable). Serving it to a person takes the gate's own deliberate override,
which is the owner's call.
