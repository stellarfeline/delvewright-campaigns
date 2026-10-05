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

A weathered carcass of bone and coral, 146 blocks long, 62 wide and up to 45
high, sunk to its belly in a mud flat on a valley floor (the piece's box is
62 × 60 × 146). The ground is part of the piece: a five-course apron of packed
mud fills its whole footprint, and the body's widest line sits a few courses
above it, so its lower flanks are a wall you cannot walk up and nothing
overhangs the mud.

World coordinates below are the built ones (the piece's origin is 0, 59, 0;
the mud is walked at y 64).

- **You arrive** on the mud on the west side (1, 64, 50), facing a wound in the
  flank: a cut four blocks high through the body at grade (z 53–57).
- **Bay A, soul lanterns** — the first room inside, centred at (31, 64, 55),
  about 26 wide and 28 long, floored by the mud. Twelve soul lanterns stand on
  its floor, two more in the wound and one at the mouth of the passage.
- **The passage** runs south from bay A to bay B (x 29–33, z 66–81), with one
  soul lantern (z 73) and one crying obsidian block (z 76) at its middle.
- **Bay B, crying obsidian** — the second room, centred at (31, 64, 90), about
  22 wide and 24 long. Eleven crying obsidian blocks stand on its floor.
- **The way up** is a stair cut into the east flank: it starts on the mud by
  the tail (43, 64, 136), climbs north along the flank and onto the back, and
  ends near the head (34, 101, 44). It is the only way onto the body.
- **The back**: the top of the body, open to the sky, walked to (31, 104, 38).

Both bays are lit only by the lights placed in the form; neither has a cut to
the sky. The two light blocks emit the same level (10) and stand on a similar
grid, about six blocks apart, so the two rooms differ mainly in the block that
gives the light.

## What to look for

1. **At the spawn**, look along the body: does it read as one beached animal at
   this scale, or as a hill with stairs on it?
2. **Walk in through the wound** into bay A. Stand in the middle and look round:
   does the soul-lantern light read as the body's own light, or as lanterns set
   down in a cave?
3. **Walk south through the passage** into bay B and do the same with the
   crying obsidian. Compare the two rooms: which one belongs to the inside of a
   body? This is the open craft question the level exists to answer.
4. **Go back out**, walk round the tail to the stair on the east flank and
   climb it. Does the stair read as cut into the body?
5. **Walk the back** to its end over the head, and look down from the edge:
   the fall to the mud is one you can see coming.

## State

Builds on the engine branch `feat/organic-giant`. The quest walks the spawn,
bay A, bay B and the back in order; the build proves the route
(`DW0311`), finds no place a body can get into and not out of (`DW0921`: 0 of
16133 reachable cells), and measures every walkable cell inside lit
(`DW0210`). `delvec sculpt` itself reports `pockets: 0 place(s)` and all four
standing anchors reached from grade.

Serve it with the engine's playtest server:

    tools/creator/playtest-server.sh up campaigns/the-beached-thing --prefabs demos/the-beached-thing/prefabs

It is never copied into a singleplayer save.

The machine ladder on the `validation/` image: PackTest passed, and the
mineflayer critical path passed (5 steps: spawn, bay A, bay B, the back; its
die-retry and death-loop stages did not run, because the level declares no
combat and no death plan). The staging gate refuses it with four findings
about objects this demo does not author — a cast (isl-35, isl-46) and an
approved design record (drill3-01, drill3-03) — so serving it to a person
takes the gate's own deliberate override, which is the owner's call.
