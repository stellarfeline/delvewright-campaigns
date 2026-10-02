# The Threshold

The demo level for **a place's own sky** (spec-0080): `world.atmospheres[]`,
a place carrying one from the first tick (`boxes[].atmosphere`), and the
`set-atmosphere` beat that repaints a place with another.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-threshold/

## What it is meant to show

One open stone hall, cut in two by a door. The near half stands under the
ordinary noon. Past the door the air is wrong from the first tick: an olive
sky, fog from one block to twenty-six, red clouds, stars at noon, ash and
crimson spores in the air, no music, soul-sand-valley ambience, dead grass
and dark water, and no rain. A bell stands in the middle of the far half.
Ringing it repaints the near half with the same sky, so the walk back is
through the place the party came from, and it is no longer there.

The far half's sky is `atmosphere/wrong-place`: the eldritch-visuals lab's
station-2 block, adopted verbatim — every attribute, the tint, `temperature`
0.8 and `downfall` 0.4 (declared as `climate`), and `precipitation: none`.

## What to look for

- **Crossing the door.** The fog and the sky change around you without
  leaving the hall. The change happens across one 4-block biome cell at the
  doorway: fog blends by your biome-blend setting, grass tint does not.
- **Stars at noon** overhead in the far half, and red clouds.
- **The bell.** The near half turns as soon as it rings — no chunk reload,
  no F3+A — and the walk back is under the wrong sky.
- **What a biome cannot do.** The sun keeps its course: the overworld's day
  cycle moves it whatever the place says.

## The four attributes the lab never set

`visual/cloud_height`, `visual/default_dripstone_particle`,
`visual/water_fog_start_distance` and `audio/firefly_bush_sounds` are not in
the station-2 block, and this level carries that block verbatim, so it does
not show them. They are compiled and loaded (the engine's gallery sets all
twenty), and their first look needs blocks this hall does not have: hanging
pointed dripstone, standing water and firefly bushes.

## State

Builds on the engine branch `feat/area-atmosphere`. The machine ladder on the
`validation/` image: PackTest's `atmosphere_places` and
`atmosphere_repaint_0` read the server's own biome inside and outside the far
half and before and after the bell; the mineflayer critical path rings the
bell and asserts the client was told by `chunk_biomes`, with no chunk reload.

To walk it in a test world, copy the build's `datapack/` into the save's
`datapacks/` as `the-threshold`, then open the world: biomes load only when a
world opens, so `/reload` is not enough. The hall stands at x 8200–8215,
z 8196–8236, y 64, away from anything near the origin.
