# The Thing Beyond the Fog

The demo level for **a cutscene that tears the fog open**: a ferry crossing
under fog and storm, a camera that rises out of the boat toward something in
the sea, a lightning bolt, and the fog cut away for one second to show it.

It confirms one new capability, `lightning` (engine spec-0092), and shows that
the rest of the scene is built from what the engine already has: `cutscene`,
`set-atmosphere` (spec-0080) in a `sequence`, the ferry's link (spec-0083) and a
body sculpted from a form (spec-0087).

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-thing-beyond-the-fog/

The figure is sculpted from a committed form, which is the artifact of record;
the structure parts beside it are what the form sculpts to:

    demos/the-thing-beyond-the-fog/forms/the-thing-beyond-the-fog.json   # the form
    demos/the-thing-beyond-the-fog/prefabs/                               # its output, regenerated, never edited

    rm -rf demos/the-thing-beyond-the-fog/prefabs
    delvec sculpt demos/the-thing-beyond-the-fog/forms/the-thing-beyond-the-fog.json -o demos/the-thing-beyond-the-fog/prefabs

Build it with `--prefabs demos/the-thing-beyond-the-fog/prefabs`.

## What it is

A strait under a thunderstorm and fog so thick the far shore is gone. Two
jetties face each other across it, forty-eight blocks apart; each is a stone
quay with a spruce deck, a railing all round with lanterns on its posts, a
rocky bank behind, and a slip in its north end with a ferry moored in it — a
dark-oak hull three wide, fence rails along both gunwales, a stem post at the
bow. The slip's mouth is closed by a boom of piles, so nobody swims out.

- **The near jetty** (play space x 8200–8211, z 8292–8307, deck at y 63) is
  where you arrive. The ferry's stern well is the hull cell (8204, 64, 8298);
  the tiller is the floor lever just astern of it (8204, 64, 8299).
- **The far jetty** (x 8248–8259) is where the ferry puts you down
  (8252, 64, 8298), its own ferry moored beside you.
- **Out on the open sea**, thirty blocks north of the near jetty, a third ferry
  drifts with a lantern at its bow: the boat the cutscene's camera starts in.
- **The Thing**, a hundred and forty blocks out, stands on the sea floor
  (piece origin 8170, 54, 8130) and rises 96 blocks from it: waist-deep in the
  sea, an octopus mantle bent forward onto hunched shoulders with no neck, a
  beard of feelers hanging over the chest, long narrow bat-like wings raised
  behind, its east claw raised and its west claw gripping the water, and two
  slanted eyes of ochre froglight. It is built for one side only — the one its
  camera sees; the form's box ends behind it, and that face is its flat back.

Both jetties carry `atmosphere/sea-fog` from the first tick: fog from the eye
to 32 blocks, the sky and the clouds under it too. From either jetty the Thing
is far inside the fog.

## The cutscene

Pull the tiller. The ferry's link (one repeatable `use` trigger, as in The
Ferry) plays one `sequence`:

| tick | what happens |
|---|---|
| 0 | the volume round the camera's path is painted `atmosphere/sea-fog`; the camera cuts to just behind the drifting ferry's stern, at a standing eye, and rises up and out toward the Thing for six seconds |
| 121 | the camera stops at its set point, 68 blocks from the figure's face, aimed where it was aimed while it rose (one `look_at` for both shots, so the hold is not a cut) |
| 141 | **a bolt strikes the sea beside the figure's raised wing** (8268, 63, 8128), and in the same tick the volume is painted `atmosphere/torn-fog`: the fog end leaves the camera and the figure stands in the flash |
| 161 | the volume is painted `atmosphere/sea-fog` again: the figure is gone into the fog |
| 222 | the camera returns everyone to where the puller stood |
| 223 | whoever is in the hull is carried to the far jetty; `flag/seen` is set |

**It plays once.** Every step of the reveal is guarded on `forbids
flag/seen`, and the flag is set with the carry. A later pull — a player who
stayed on the jetty, boarding afterwards — plays no cutscene: whoever is in
the hull is blinded for twelve seconds, told *the ferry slides out into the
fog*, and carried.

## The fog flash, measured

The owner asked for the fog to be removed *briefly*. Whether a one-second
reveal reads as a flash or as a slow fade is a property of the client, so it
was measured on both legs of the path from the server to the screen.

**The network leg** — a mineflayer client (the harness pin, 4.37.1) on the
pinned validation server running this build, boarding the ferry and pulling the
tiller as itself, every packet stamped on one monotonic clock
(`measure/fog-net.sh`, `measure/fog-timing.mjs`; readings in
`measure/fog-timing.json`). After the pull:

| ms after the pull | packet |
|---|---|
| +117.9 | 16 `chunk_biomes` packets, 48 distinct chunks — the tick-0 paint |
| +134.0 / +153.3 | spectator mode; the camera |
| **+7145.8** | **the bolt** (`spawn_entity minecraft:lightning_bolt` at 8268.5 63 8128.5) |
| **+7145.9** | **16 `chunk_biomes` packets, 48 chunks — the fog torn away** |
| +8144.5 | 16 `chunk_biomes` packets, 48 chunks — the fog back |
| +11189.9 | adventure mode again: the camera has returned |
| +16140.1 | the client stands at 8252.5 64 8298.5, the far landing |

The bolt and the torn fog reach the client in the same server tick, 0.1 ms
apart; the fog returns 998.6 ms (20 ticks) later.

**The client leg** — what the client does with a repaint, read through its own
classes (`measure/FogFlash.java`; readings in `measure/client-readings.txt`).
The pinned client's `GaussianSampler`, `SpatialAttributeInterpolator` and
`EnvironmentAttributeMap` are called from its jar at the camera's two poses,
and the `fog_end_distance` type's own partial-tick `LerpFunction` — the
function `EnvironmentAttributeProbe$ValueProbe.get` applies between the
previous client tick's value and the current one — across the tick a repaint
lands in. At both poses the repainted volume holds the whole kernel (weight
1.000000000000), and through `AtmosphericFogEnvironment.setupFog`'s rain
offset (transcribed from its bytecode; both atmospheres rain, so the rain fog
multiplier does not move):

| client frame | effective fog | fog over the boat (4) / at 32 / on the figure (68) / at 100 blocks |
|---|---|---|
| the tick before | −10 → 32 | 0.333 / 1.000 / 1.000 / 1.000 |
| ¼ into the next | −10 → 96 | 0.132 / 0.396 / 0.736 / 1.000 |
| ½ | −10 → 272 | 0.050 / 0.149 / 0.277 / 0.390 |
| ¾ | −10 → 520 | 0.026 / 0.079 / 0.147 / 0.208 |
| the tick after | −10 → 768 | 0.018 / 0.054 / 0.100 / 0.141 |

So the figure goes from wholly fogged to nine-tenths clear inside one client
tick (50 ms), holds for a second while the bolt flickers, and is gone again
inside one tick. **It is a flash, not a fade.**

Two choices in the atmospheres follow from this reading. `fog_start` is 150 so
that, under the storm's rain offset of −160, the fog starts at the eye rather
than 160 blocks behind it; and the two atmospheres share `precipitation`,
because a change of precipitation would ease the rain fog multiplier over
about a second and turn the cut into a fade.

The instrument committed here differs from the one run only in where it finds
`tools/lib/rcon.mjs` (an env var instead of a path in the scratch tree).

## How the figure is made to read

Researched, not invented; each rule says which.

- **Lovecraft's own description** (cited — *The Call of Cthulhu*, 1928, public
  domain in the United States; Project Gutenberg #68283): "an octopuslike head
  whose face was a mass of feelers, a scaly, rubbery-looking body, prodigious
  claws on hind and fore feet, and long, narrow wings behind"; the idol's
  "cephalopod head was bent forward"; at sea, "a mountain walked or stumbled".
  So: the mantle, the feelers, the claws, the long narrow wings, the head bent
  forward, and a scale that reads as a landscape.
- **The silhouette carries the reading** (cited — World of Level Design,
  *Silhouette Design for Game Environments*, as The Beached Thing cites it): a
  form that reads at a distance is recognisable from its outline alone, built
  as a hierarchy of large, medium and small shapes. Large: the torso and the
  raised wings, which make the outline a V over a mass; medium: the mantle and
  the raised claw; small: the feelers, the finger-bones of the wings, the eyes.
- **No neck** (ideas only — Tomeu Riera's Cthulhu concept, unlicensed): a
  creature this size reads as massive when the head sits low on the shoulders.
- **The wings are bat wings, not feathered or rounded** (authored, after the
  first sculpt read as a fairy's): a membrane drawn as a polygon from the
  shoulder blade along the arm of the wing to the wrist, out to four finger
  tips, scalloped between them, with the bones standing proud of it.
- **The feelers splay and alternate** (authored, after the second sculpt
  merged them into one green bib): eight, each hanging further the nearer it
  is to the centre, spreading as they fall, alternate ones a course forward.
- **Tone** (cited — Lovecraft: "soapy, greenish-black" stone with "golden or
  iridescent flecks"): dark prismarine, polished deepslate, polished blackstone
  with gilded blackstone, blackstone; the feelers in dark prismarine with
  prismarine bricks, so they read against the chest.
- **The eyes glow** (engine — spec-0087 hand lights): eight cells of ochre
  froglight set into two slanted cut sockets, the inner end lower.

`review/reveal-frame.png` is the frame the camera holds when the fog is torn:
the pinned Chunky core (`chunky-core-2.5.0-SNAPSHOT.474.g156e2bb`, 260 spp)
over this build's world save, the scene `delvec panorama` emits re-posed at the
camera's set point (8212.5, 86.5, 8226.5, yaw −177.7, pitch −6.9, fov 70) —
`review/reveal-frame.scene.json`, its world path written as `<build-dir>/world`, the save `validation/world-save.sh` writes. Chunky
draws neither biome fog nor entities, so it shows the instant the fog is gone
and not the bolt.

## What to look for

Serve it with the engine's playtest server, from the engine branch
`feat/the-thing-beyond-the-fog` (the verb is not in a released engine), and
look at it in a real client — the fog, the flash and the bolt are client-side
and no render can show them.

1. **You arrive on the near jetty** (8205, 64, 8299) in fog and rain under a
   thunderstorm. Nothing beyond about thirty blocks is visible. The ferry is in
   the slip in front of you.
2. **Choose the passenger's kit, then step down into the ferry's stern well** (8204, 64, 8298) — *Board the
   ferry*. Then **pull the tiller**, the lever astern of the well.
3. **The cutscene** (eleven seconds): the camera starts just behind a ferry
   adrift in the fog, its bow lantern ahead, and rises up and out toward the
   north. Look for: the drifting ferry reading as *your* boat; the climb being
   smooth; the camera stopping and holding.
4. **One second into the hold, a bolt strikes beside the figure's raised
   wing.** Look for: the bolt, the sky flash and the thunder arriving together
   with the fog being cut away; **whether the figure reads at first sight as a
   colossal octopus-headed thing with wings and glowing eyes**; whether one
   second is long enough; whether the cut reads as a flash rather than a fade.
5. **The fog closes; the camera returns; you are on the far jetty**
   (8252, 64, 8298) — *Cross the strait*, and the delve completes. Look for:
   the one or two frames of the near jetty between the camera's return and the
   carry (the same seam The Ferry has).
6. **With a second player**, leave them on the near jetty: they watch the
   cutscene too, come back where the puller stood, and are carried with them.
7. **Pull the tiller a second time** (a fresh join, or a player who stayed
   behind and boards afterwards): no cutscene — twelve seconds of blindness,
   *The ferry slides out into the fog.*, then the far jetty.

## What the compile says

On the engine branch at `bcac1165e` (delvec 1.8.1, dsl 0.36.0):

    lightning binding: 1 strike(s) declared, 1 struck block(s) read, 1 post(s) within reach examined, 0 refused
    DW0311 binding: 4 leg(s); 3 walked, 0 carried by a crossing, 1 carried by a link, 0 carried by a loop; 1 link(s) declared, 1 live on some leg, 1 taken; 0 gather(s) declared
    DW0921 binding: 1 quest configuration(s), 6 route cell(s), 358 cell(s) a body can reach by walking, falling, jumping or swimming (28 of them afloat), 0 it cannot leave; 0 link stand cell(s) served as a way out

The 28 afloat cells are the two slips' side channels, each with a step at its
stern end; nothing reaches the open sea. Setup holds the strike's chunk
(`forceload add 8268 8128 8268 8128`). The figure sculpts with 0 pockets and
1 component kept.

## State

- **Machine ladder** on the `validation/` image, engine `bcac1165e`, content
  `4656f6f`: PackTest **21 of 21 required tests passed**, `lightning_0` and
  `atmosphere_places` among them; the mineflayer critical path **passed, 5
  steps** — boards the hull, pulls the tiller from its stand cell, waits out
  the cutscene and is carried.
- **Staging gate**: REFUSED on two findings, both the design record the level
  does not carry (`drill3-01`, `drill3-03`): no approved image under `design/`.
  An approved image is the owner's to give; it is not overridden.
- **Not yet looked at by a person**: everything in *What to look for*.
