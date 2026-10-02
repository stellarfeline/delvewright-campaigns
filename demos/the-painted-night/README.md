# The Painted Night

The demo level for **a delve wearing its own textures** (spec-0084):
`world.textures[]`, a row replacing one vanilla texture through the resource
pack the delve ships, for the whole delve, under a recorded licence.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-painted-night/

## What it is

A meadow in a valley at midnight, under a clear sky, in two halves joined by
open grass.

- **The meadow** (x 8200–8247, z 8200–8231, ground at y 64). You arrive in its
  middle.
- **The shore** (x 8200–8247, z 8233–8264), south of it. When you have looked
  up, a drowned takes its place at the shore's middle and stands there, facing
  north. It does not move and cannot be hurt.

Two textures are replaced:

| Row | Replaces | The image |
| --- | --- | --- |
| `red-moon` | `minecraft:environment/celestial/moon/full_moon` (32×32) | a plain red disc on a transparent ground |
| `shore-walker` | `minecraft:entity/zombie/drowned` (64×64) | flat lilac bands, a dark band every eighth row |

**Why the full moon.** The world is played at `midnight` and its clock does not
advance. The pinned client's moon timeline (`data/minecraft/timeline/moon.json`
in the 1.21.11 jar) holds `minecraft:visual/moon_phase` at `full_moon` from
tick 0 to tick 24000 — the first day, the only day this delve has — so the
moon over this valley is the full moon, and that is the texture the row
replaces.

**The images are original.** `demos/the-painted-night/draw-textures.py` draws
both from nothing and writes them into `campaigns/the-painted-night/textures/`;
it reads no vanilla pixel, and writes its PNGs by hand (stored deflate, no
compressor), so the same bytes come out on every machine. Both rows record
`license: {spdx: original, source: original}`.

## What to look for

Accept the resource-pack prompt when you join. The pack is served by the
server: it is applied while you are connected and gone when you leave, and
your own resource packs are untouched.

1. **Look up.** The moon is a plain red disc, not the grey full moon.
2. **Walk south to the shore.** The drowned standing there is lilac and
   striped, not the green-blue of a vanilla drowned.
3. **Walk back north** to where you started; the walk ends there.
4. **Leave and join any other world.** The moon and the drowned are vanilla
   again — the pack went with the server.
5. **Decline the pack** on a second join: the moon is grey and the drowned is
   vanilla, and the walk is just as finishable.

Nothing a render can show: the pinned Chunky core draws no moon and no drowned.
The comparison sheets `delvec textures campaigns/the-painted-night` writes
(vanilla on the left, this delve's on the right) are what to read beside the
walk; they contain vanilla's pixels and are never committed.

## State

Built by the engine branch `feat/texture-overrides`. The machine ladder on the
`validation/` image:

- **PackTest**: all 18 required tests passed.
- **The mineflayer critical path** passed (5 steps). The bot was pushed the
  pack the build made: one push of `http://pack:8000/resourcepack.zip` with
  sha1 `2fa9a50e31c453356f218b4a316af0f5ee8f0ac1`, downloaded from that URL
  to the same sha1, equal to the build's `resource_pack_sha1`. Pointed at a
  URL the sidecar does not serve, the same run fails: the push downloads
  nothing and the bot refuses the run.

The level is served with the engine's playtest server
(`tools/creator/playtest-server.sh up campaigns/the-painted-night`), which
serves the pack from its sidecar and never installs it; never copied into a
singleplayer save. Its staging gate refuses it on five findings about objects
the level does not author — a quest `cast` (isl-35, isl-46), a design record
(drill3-01, drill3-03) and actor equipment (doune-04) — so serving it takes
the gate's own deliberate override, which is the walker's call.
