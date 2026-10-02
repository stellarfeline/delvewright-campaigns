# The Threshold

The demo level for **a place's own sky** (spec-0080): `world.atmospheres[]`,
a place carrying one from the first tick (`boxes[].atmosphere`), and the
`set-atmosphere` beat that repaints a place with another.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-threshold/

## What it is

A meadow in a valley, with an unmarked line across it. Both sides carry the
same things, so every change is seen against its twin: grass, ferns, five oaks,
firefly bushes, a stone cistern three blocks deep, and a gate of two stone
pillars whose dripstone lintel hangs three pointed dripstone tips over the gap.

- **The near meadow** (x 8200–8247, z 8200–8231, ground at y 64) is the
  horizon's ordinary noon, behind a two-course garden wall on three sides. You
  arrive at its centre (8223, 64, 8215).
- **The line** is z 8232, the whole width of the meadow. Nothing marks it but
  the sky.
- **The far meadow** (x 8200–8247, z 8233–8288) is open to the valley floor on
  its three outer sides; the valley's slopes and rim close the view. Its sky is
  wrong from the first tick: `atmosphere/wrong-place`, the eldritch lab's
  station-2 block (olive sky, fog from one block to twenty-six, red clouds,
  stars at noon, ash and crimson spores, no music, soul-sand-valley ambience,
  dead grass and dark water, no rain), plus the four attributes the lab never
  set — clouds at y 96, lava drips from pointed dripstone, water fog starting
  two blocks out, and firefly bushes that sound at noon.
- **The bell** stands at the far meadow's centre (8223, 64, 8260). Ringing it
  repaints the near meadow with the same sky, so the walk back is through the
  place you came from, and it is no longer there.

| Thing | Near | Far |
| --- | --- | --- |
| Cistern (water x 8204–8212, three deep, y 64–66; steps on its east side) | z 8211–8219 | z 8256–8264 |
| Dripstone gate (pillars at x 8235; tips at y 67) | z 8212–8218 | z 8257–8263 |

## Why the first build showed no fog, and what changed

The client does not read fog from the biome you stand in. It averages every
4-block biome cell within twelve blocks of the camera, up and down included,
and a cell that sets no fog end counts as 1024 blocks. The first build painted
only the far hall's own air, eight blocks tall, so the camera never stood more
than 56% inside its sky and the fog end read about 467 blocks. The engine now
paints a place as far as the camera inside it reads, and this level is big
enough for that: the fog is whole from z 8242 to the far end, between x 8202
and 8245. Every build prints the measurement as an `atmosphere reach` line
(this one: 2068 of 2688 standing eyes read the far sky whole).

## What to look for

1. **At the spawn**, the near meadow is an ordinary noon: blue sky, white
   clouds high up, green grass and oaks, clear water in the cistern.
2. **Walk south down the middle towards the bell.** Over the ten blocks past
   z 8232 the air thickens; from z 8242 on, the fog closes at about twenty-six
   blocks. The valley rim, which you could see from the near meadow, is gone,
   and the oaks and the far end fade out at that depth.
3. **Look up**: stars at noon, red clouds low overhead (y 96, not the usual
   192), and the olive sky.
4. **Look down**: the grass, ferns and oak leaves are the dead yellow-brown of
   the far sky, against the green behind you. The grass tint changes in
   4-block steps at the line; the fog does not step.
5. **The far cistern**: climb the two steps on its east side and drop in. The
   water is dark, and the underwater fog closes within about six blocks; the
   near cistern's water is clear.
6. **The far dripstone gate** (east of the path, x 8235): watch the three tips
   for a while. They drip lava. The near gate's tips drip water.
7. **Listen** by a far firefly bush: they chirp at noon. The near ones are
   silent until night. No music, and the soul-sand-valley ambience.
8. **Ring the bell.** The near meadow turns at once — no chunk reload, no
   F3+A. Walk back to the spawn: the near meadow is now under the same fog and
   sky, and its cistern, gate and bushes behave like the far ones.
9. **What a biome cannot do**: the sun stays where noon puts it in both
   meadows.

## State

Builds on the engine branch `feat/area-atmosphere`. The machine ladder on the
`validation/` image: PackTest's `atmosphere_places` and `atmosphere_repaint_0`
read the server's own biome inside and outside the far meadow and before and
after the bell; the mineflayer critical path rings the bell and asserts the
client was told by `chunk_biomes`, with no chunk reload.

The level is served with the engine's playtest server
(`tools/creator/playtest-server.sh up campaigns/the-threshold`), never copied
into a singleplayer save. Its staging gate reports six findings about objects a
demo level does not author (an item-gated interaction and a cast: isl-02,
isl-35, isl-41, isl-46; a design record: drill3-01, drill3-03), so serving it
takes the gate's own deliberate override.
