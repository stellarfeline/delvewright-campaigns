# The Beached Thing

The demo level for **a body the size of a hill** (spec-0087): a prefab sculpted
by `delvec sculpt` from a declared form, lying on its own ground, walked inside
and onto its back by the proofs the engine already has. The body is a rotting
sperm whale, stranded on a mud flat.

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

A sperm whale 143 blocks from snout to fluke notch, lying on its belly in a mud
flat on a valley floor, with a bank of mud standing off its west flank to look
at it from. The piece's box is 148 × 60 × 146. The body fills its east 55
blocks (x 90–144): it is 32 blocks across the flanks at the mud, and stands 28 high at the
head (33 at its highest weathered block). The ground is part of the piece: a
five-course apron of packed mud fills the whole footprint.

At this scale one metre of a 15 m bull is about 9.5 blocks. Its parts, as the
form declares them (snout north, tail south):

- **The head** is the front third of the body: a tall, squared block with a
  blunt, nearly vertical front and a flat top, standing a little higher than
  the back behind it. The blowhole is a slit on the left of the crown at the
  front. A small eye sits low on each side, at the back of the head.
- **The lower jaw** is narrow and long. It has fallen slack from under the
  head, swung out onto the mud on the west side, and its bone is bare, with a
  row of teeth along it.
- **The trunk** is widest just behind the head and spreads on the mud under
  its own weight, so the lower flanks bulge out over the ground.
- **Two small paddle flippers** lie splayed on the mud, one on each flank,
  just behind the head.
- **The dorsal hump** is low and thick, two thirds of the way back. Behind it
  a row of knuckles runs down the tail stock.
- **The rump** is bloated. It stands over the root of the tail as a wall
  several blocks high, so the tail is not a ramp onto the back.
- **The tail stock** narrows to **the flukes**, which lie flat on the mud, 37
  blocks from tip to tip, with a notch between them.
- **The wound** is on the west flank over bay A. The hide is torn away round a
  ragged rim of red flesh, and six ribs show in the hollow behind it, slanting
  back as they go down. Two of them are broken off and hang over the way in.
  Further back on both flanks, the ribs show as ridges under the dried hide.

Every part of the body declares its own material, so the tones follow the
anatomy, not the sculpt's shading. Each hide tone is one full block, with a
stair and slab family of nearly the same mean colour, so no tone is single-block
noise:

- **Hide**: one dark slate grey over the whole body: the head, the back, the
  flanks, the flippers and the flukes. Gray concrete, with deepslate-tile stairs
  and slabs.
- **The lower flanks**, where the trunk spreads on the mud, are a slightly
  darker, browner grey: gray terracotta, with polished-blackstone stairs and
  slabs.
- **Sloughed skin**: five large pale-grey areas with defined edges, on the back
  and the upper flanks: two along the back, one on the upper west flank above
  the wound, one on the west flank before the rump, and one on the crown of the
  head. Light gray concrete, with stone stairs and slabs. It is grey, not white.
- **The fluke edge** is one row of a lighter grey round each lobe (cyan
  terracotta, with cobbled-deepslate stairs and slabs), so the flukes show
  against the mud.
- **Bone** (bone block and calcite, with pale-oak stairs and slabs) is only
  where bone is bare: the lower jaw, its teeth and the ribs in the wound.
- **Red-brown flesh** (red, brown and pink terracotta, nether wart block) is
  only on the rim of the wound and on the inside walls of the bays and the
  passage.

The mud bank is its own material (packed mud,
coarse and rooted dirt, mud-brick steps), so it reads as ground, not as part of
the animal.

World coordinates below are the built ones (the piece's origin is 0, 59, 0;
the mud is walked at y 64).

- **You arrive** on the mud between the bank and the body (36, 64, 64), facing
  the body.
- **The vantage** is a bank of mud on the valley floor west of the body, with
  a worn path up its east side to a flat top at (16, 69, 71). From there the
  whole whale lies broadside in front of you. It spans 79 degrees of the
  horizon (Minecraft's default field of view shows about 102 at 16:9) and 18
  degrees of height, from 74 to 139 blocks away. That is inside the served
  view distance of 10 chunks: its farthest block is 8.7 chunks off.
- **The wound and the way in** is a cut through the hollow at grade
  (x 85–108, z 52–56), between the broken ribs.
- **Bay A, soul lanterns** is the first room inside, centred at
  (117, 64, 55), 19 wide and 28 long. A mass of flesh stands in its middle
  from floor to vault, so the floor is a ring about four blocks wide round it.
- **The passage** runs south from bay A to bay B (x 115–118, z 66–80), three
  blocks high.
- **Bay B, crying obsidian** is the second room, centred at (117, 64, 90),
  18 wide and 24 long, with two columns of flesh standing in it.
- **The east door** leaves bay B at grade (x 119–138, z 99–103) and passes
  under the stair out onto the mud of the east flank.
- **The way up** is a stair cut along the east flank. It starts on the mud
  beside the tail stock (122, 64, 116), climbs north along the flank's own
  contour with its outer side open to the sky, passes over the east door, and
  comes out on the back behind the head (117, 87, 56). It is the only way onto
  the body: sculpted without it, the walk from grade does not reach the back.
- **The back** is the top of the body, open to the sky, from behind the head
  south along the spine to the hump.

### The light inside

No lantern stands on a floor. Every source inside is set into the body's own
surface by the sculpt (`lights[].hull`, spec-0087 §9), drawn as a seeded
Poisson-disk scatter — staggered and irregular, never a grid — over walls and
vault:

- **Bay A** has soul lanterns, **recessed**. Each sits one block behind the
  surface, hidden behind a polished-granite stair set in the surface, with a
  one-block slot beside the stair through which its light comes out. A dense
  band at floor height (38 sources, spacing 2.75) lights the floor. A second
  entry over walls and vault (54 sources, 14 of them in the vault, spacing 3)
  lights the upper space. The light reaches the room at level 7 in front of
  each slot.
- **Bay B** has crying obsidian, **embedded**: flush in the surface, a block
  of the wall or vault itself (57 sources, 37 wall and 20 vault, spacing 3.5).
- **The passage** (4 sources) and **the hollow of the wound** (12 sources)
  have soul lanterns, recessed, as in bay A.

So the two rooms differ in kind as well as in block: bay A is lit by hidden
lanterns, bay B by a glowing body. The research behind these rules and their
numbers is in the engine's `docs/reference/interior-lighting.md` §7.

## How the body is made to read

Researched, not invented. Each rule below says whether it is cited or
authored.

### The species

- **A sperm whale** (cited). Its head is about one third of its total length
  and its lower jaw is narrow ([NOAA Fisheries, *Sperm Whale*][noaa]). Those
  two features read at a distance from the outline alone, which no other whale
  offers as strongly. The tall, squared forehead also carries the campaign's
  brow stone, and its blowhole, ribs and long lower jaw match the design.

### Proportions

Every length is a fraction of total length (TL, snout tip to fluke notch). The
form scales TL to 142 blocks.

| Feature | Value used | Source |
|---|---|---|
| Head length | 34% TL; the head capsules end at 0.34 TL | Fujino 1956 No. 20, severed head 35.1% (males 15–16 m); NOAA "about one-third" |
| Snout projecting past the jaw tip | 7% TL | Fujino No. 2, 7.05% |
| Blowhole | 4.5% TL, on the left of the crown | Fujino No. 3, 4.2%; NOAA, left side |
| Angle of the gape | 26% TL | Fujino No. 4, 24.5%; Degrati 395/1470 = 27% |
| Eye | 29% TL | Fujino No. 5, 28.2%; Degrati 440/1470 = 30% |
| Flipper insertion | 41% TL | Degrati 580/1470 = 39.5% |
| Flipper length, width | 9.5%, 4.7% TL | Degrati 140/1470 and 69/1470; Fujino No. 19, 4.6% |
| Maximum girth | 79% TL at 0.40 TL, measured round the form's section, buried belly included | Degrati 880/1470 = 60%; the excess is authored (below) |
| Dorsal hump | at 62% TL, about 3 blocks high, 9.5% TL long | Degrati, fin base 898/1470 = 61%, base 140/1470; Fujino No. 14, height about 2% |
| Girth at the anus | 56% TL at 0.74 TL, measured as above | Degrati 540/1470 = 37%; the excess is authored (below) |
| Fluke spread | 26% TL | Fujino No. 25, 23.8–26.5%; Degrati 412/1470 = 28% |
| Fluke chord at the insertion | about 7% TL | Fujino No. 9, 7.3% (Bonin) |
| Teeth | 8 a side at block scale | NOAA: 20–26 a side |

Sources: [Fujino, *On the Body Proportions of the Sperm Whales*, Sci. Rep.
Whales Res. Inst. 11, 1956, Table III][fujino] and [Degrati et al., *New
record of a stranded sperm whale*, Mastozoología Neotropical 18(2), 2011,
Table 1][degrati]. Both are **ideas-only** (ADR-0013): Fujino's paper states
no licence, and Degrati's journal is CC BY-NC. Only measured numbers are used.
No text, table or figure of either is reproduced.

**The trunk is fatter than a live whale** (authored). Its girth is 79% of
length behind the head and 56% at the anus, against 60% and 37% measured. Part
of the excess is the sag and the bloat below, which are cited effects; the rest
is the room the two bays need inside walls thick enough to hold their lights.

### The carcass

- **It lies on its belly** (authored). On a beach a carcass may lie on its side
  or roll ([Moore et al., *Dead Cetacean? Beach, Bloat, Float, Sink*,
  Frontiers in Marine Science, 2020][moore], CC BY 4.0). The belly-down lie is
  chosen so the back is a walkable ridge.
- **The trunk sags and spreads** (cited for the effect, authored for the
  amount). A beached minke carcass became "flatter and more collapsed" after
  five months, with "skin draped over bones" ([Baptist et al., *Decomposition
  of a minke whale carcass in a temperate dune ecosystem*, Frontiers in Marine
  Science, 2025][minke], CC BY 4.0). Here a wide, flat solid under the trunk
  spreads its lower flanks over the mud.
- **The head stands highest** (authored, unsupported). The form assumes the
  spermaceti case and junk keep their shape while the trunk sags. No source in
  hand says so.
- **The rump is bloated** (cited for the effect, authored for its place).
  Decomposition gas distends a carcass ([Moore et al.][moore]). The form puts
  the swelling over the tail root, where it also stops the tail being a ramp
  onto the back.
- **The jaw is bare bone** (cited). On the minke, birds pecked the mandibles
  bare first, within two months, and its jawbones and most vertebrae were
  bare by eighteen months ([Baptist et al.][minke]).
- **Ribs show** (cited). Rib contours showed through the minke's skin at seven
  months ([Baptist et al.][minke]). The open wound with exposed ribs is
  authored: it is where the way in is.
- **One dark grey hide** (cited). Sperm whales are "mostly dark grey"
  ([NOAA][noaa]).
- **Sloughed skin in a few pale areas on the back** (cited for the effect and
  its place, authored for the amount). On the minke the "epidermis detaching"
  came at two months, and birds marked it "particularly on the back"
  ([Baptist et al.][minke]). The record gives no area, so the number and size
  of the patches are authored. The sperm whale's head carries pale scars from
  fights ([Degrati et al.][degrati], ideas-only), which is why one patch is on
  the crown.
- **A lighter fluke edge** (cited). At three weeks the minke's "tail edge
  discolored light grey" ([Baptist et al.][minke]).
- **Bone white only where bone is bare, flesh red only where the body is
  open** (authored). Scattering bone and flesh tones over the hide read as
  camouflage: the outline was lost in it.
- **The knuckles** behind the hump are from [SEASWAP, *Sperm Whale
  Anatomy*][seaswap], which states no licence and is ideas-only.

### Reading at a distance

- **The silhouette carries the reading** (cited). A form that reads at a
  distance is one recognisable from its outline alone, built as a hierarchy of
  large, medium and small shapes ([World of Level Design, *Silhouette Design
  for Game Environments*][wold]). Here the large shapes are the squared head
  and the trunk. The medium shapes that break the outline are the hump, the
  tail stock and flukes, the flippers and the jaw. The small ones are the
  knuckles and ribs.
- **A walkable carcass is flesh, bone and earth** (cited). Monster Hunter:
  World's Rotten Vale is a valley formed by the remains of a giant serpent,
  its caverns "decorated with pale earth, tan rotting flesh, and bloody
  remains" ([Monster Hunter Wiki, *Rotten Vale*][vale]). Hence red-brown flesh
  inside the body and round the wound.
- **No pale stone on the body** (authored). A pale stone-and-coral palette
  read as a boulder from afar and a cliff from the ground. The hide's full
  blocks are concrete and terracotta; dark deepslate, blackstone and stone
  appear only as the stairs and slabs matched to them.

The engine's organic-voxel spike pins a CC0 skeleton mesh of *Cetotherium
riabinini* (`tools/spike-organic-voxel/`; `docs/ACKNOWLEDGEMENTS.md`). It is
not used here: it is an extinct baleen whale, and a skeleton, not a body.

[noaa]: https://www.fisheries.noaa.gov/species/sperm-whale
[fujino]: https://www.icrwhale.org/pdf/SC01147-83.pdf
[degrati]: https://www.redalyc.org/pdf/457/45722044013.pdf
[moore]: https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2020.00333/full
[minke]: https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2025.1474460/full
[seaswap]: https://seaswap.info/sperm-whales/anatomy/
[wold]: https://www.worldofleveldesign.com/categories/game_environments_design/silhouette-design-game-environments.php
[vale]: https://monsterhunterwiki.org/wiki/Rotten_Vale

## What to look for

1. **Look at the whale from where you arrive.** Before you climb anything, does
   it read at first sight as a beached sperm whale, rather than as a built
   mound? Look for the squared head, the jaw on the mud, the hump and the tail
   running out to the flukes.
2. **Go to the vantage.** Take the worn path up the mud bank and stand on its
   top facing east. Does the whole animal read as one body, head to flukes?
3. **Look at the wound** as you walk to it. Do the ribs read as ribs, and the
   hollow as torn flesh rather than a cave mouth?
4. **Walk in** to bay A. Stand in the ring and look round and up. Does the
   light read as the body's own, coming out of the walls and the vault, or as
   lanterns someone put there? Is the upper space lit, and does the slot of a
   hidden lantern read as part of the wall?
5. **Walk south through the passage** into bay B and do the same with the
   crying obsidian set into the walls and vault. Compare the two rooms: which
   one belongs to the inside of a body? This is the open craft question the
   level exists to answer.
6. **Go out through the east door**, under the stair. Find the stair's foot by
   the tail and climb it. Does it read as cut into the flank? On the way, look
   at where the tail leaves the body: the bloated rump should stand over it.
7. **Walk the back** from behind the head south to the hump, and look down
   from the edge: the fall to the mud is one you can see coming.

## State

Built with the released `delvec` 1.8.1 (dsl 0.35.1). The quest walks the
vantage, bay A, bay B and the back in order. The build proves the route (4 legs
walked) and finds no place a body can get into and not out of (`DW0921`: 0 of
31137 reachable cells). It measures every walkable cell lit (`DW0210` silent).

`delvec sculpt` itself reports:

- `pockets: 0 place(s)` of 22746 reachable cells;
- all five standing anchors reached from grade;
- identical bytes when sculpted twice.

Sculpted without the stair (the form minus its last solid), the walk from grade
reaches 4 of 5 anchors, and the back is not among them.

Serve it with the engine's playtest server:

    tools/creator/playtest-server.sh up campaigns/the-beached-thing --prefabs demos/the-beached-thing/prefabs

It is never copied into a singleplayer save.

The machine ladder on the `validation/` image, from the engine tree at the
1.8.1 release tag:

- PackTest passed (17 of 17 required tests).
- The mineflayer critical path passed in 6 steps: spawn, the vantage, bay A,
  bay B, the back. Its die-retry and death-loop stages did not run, because
  the level declares no combat and no death plan.

The staging gate, against that tree's findings ledger, refuses the level with
2 reds: drill3-01 and drill3-03 (14 bound, 81 inapplicable, 25 declared
uncoverable). Both are about the design record a demo level does not yet
carry. Serving it to a person takes the gate's own deliberate override, which
is the owner's call.
