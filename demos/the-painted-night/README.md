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
  north, a nautilus shell in its hand. It does not move and cannot be hurt.

The meadow is open: its shell walls are carved down to the ground on three
sides, so it runs on into the valley floor. It is turf scattered with grass,
ferns, bushes and wild flowers, and has no trees, so nothing shades it from the
moon. The shore is a cove. Its three outer sides are a rock bank, two courses
high with a broken crest, and a body cannot climb it, so the open grass is
still the only way between the two halves. A sand beach runs down to a still
pool along the far bank, with a wandering waterline. The drowned's place is on
the sand a few blocks from the water. Every block comes from `world-edits.json`.

Three textures are replaced:

| Row | Replaces | The image |
| --- | --- | --- |
| `red-moon` | `minecraft:environment/celestial/moon/full_moon` (32×32) | a plain red disc on a transparent ground |
| `shore-walker` | `minecraft:entity/zombie/drowned` (64×64) | the drowned's skin: a deep-sea fish-folk — dusk-blue scales over a pale belly, round glowing yellow eyes, a wide toothed mouth, gill slits, a coral dorsal fin from crown to spine, coral fins on forearms and calves, webbed clawed hands and feet, glowing spots along each flank |
| `shore-walker-garb` | `minecraft:entity/zombie/drowned_outer_layer` (64×64) | what it wears over the skin: a fishing net over the shoulders, a rope belt, a kelp skirt down the thighs, shell-and-coral bracelets, ankle cords, barnacles and a strand of kelp on the head; transparent everywhere else |

The drowned is drawn in two layers, the skin and a slightly larger copy of
the same model over it, so both are replaced: a skin alone leaves vanilla's
outer layer drawing its own clothes over it. Both sheets are painted face by
face on the zombie-model box layout the drowned uses (head, body, both arms,
both legs; every face of each), so the head reads as a head and the limbs as
limbs.

**Why the full moon.** The world is played at `midnight` and its clock does not
advance. The pinned client's moon timeline (`data/minecraft/timeline/moon.json`
in the 1.21.11 jar) holds `minecraft:visual/moon_phase` at `full_moon` from
tick 0 to tick 24000 — the first day, the only day this delve has — so the
moon over this valley is the full moon, and that is the texture the row
replaces.

**The images are original.** `demos/the-painted-night/draw-textures.py` draws
all three from nothing and writes them into `campaigns/the-painted-night/textures/`;
it reads no vanilla pixel, and writes its PNGs by hand (stored deflate, no
compressor), so the same bytes come out on every machine. Every row records
`license: {spdx: original, source: original}`.

## What to look for

Accept the resource-pack prompt when you join. The pack is served by the
server: it is applied while you are connected and gone when you leave, and
your own resource packs are untouched.

1. **Look up.** The moon is a plain red disc, not the grey full moon.
2. **Walk south to the shore.** The drowned standing there is a fish-folk:
   a blue-scaled body with a pale belly, big yellow eyes and a toothed mouth,
   a coral fin down its back, a net over its shoulders and a kelp skirt — and
   none of the teal clothes of a vanilla drowned.
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

- **PackTest**: all 19 required tests passed.
- **The mineflayer critical path** passed (5 steps). The bot was pushed the
  pack the build made: one push of `http://pack:8000/resourcepack.zip` with
  sha1 `2fa9a50e31c453356f218b4a316af0f5ee8f0ac1`, downloaded from that URL
  to the same sha1, equal to the build's `resource_pack_sha1`. Pointed at a
  URL the sidecar does not serve, the same run fails: the push downloads
  nothing and the bot refuses the run.

The level is served with the engine's playtest server
(`tools/creator/playtest-server.sh up campaigns/the-painted-night`), which
serves the pack from its sidecar and never installs it; never copied into a
singleplayer save. With the staging-gate ledger that reads a demo by its own
objects, the gate refuses it on two findings, both the design record it does
not yet carry (drill3-01, drill3-03); it is not overridden.
