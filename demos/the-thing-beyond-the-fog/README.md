# The Thing Beyond the Fog

The demo level for **a cutscene that tears the fog open and shows the party in
it**: a ferry on a fogbound strait under a storm, a camera that rises from
behind the party toward something in the sea, a lightning bolt, the fog cut
away, and a wide shot of the boat — with the party standing in it — and the
thing together in a clearing.

It confirms two capabilities: `lightning` (engine spec-0092) and **the party
seen in its own cutscenes** (engine spec-0095: a stand-in for each player, in
their own skin and gear, where they stood). The rest is built from what the
engine already has: `cutscene`, `set-atmosphere` (spec-0080) in a `sequence`,
the ferry's link (spec-0083) and a body sculpted from a form (spec-0087).

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
quay with a spruce deck, a railing all round with lanterns on its posts and a
rocky bank behind.

- **The near jetty** (play space x 8200–8211, z 8292–8307, deck at y 63) is
  where you arrive. A gap in its east rail (8212, 8301–8302) opens onto a pier.
- **The ferry** lies on the strait just off the near jetty's east side, in its
  slip (x 8213–8220, z 8295–8302), **bow north toward the open sea**: a
  dark-oak hull five wide with fence rails along both gunwales and round the
  bow. Its well — x 8214–8216, z 8298–8300 — is all of it inside the carry,
  so it does not matter where in the boat you stand. The pier on piles runs
  from the jetty's gap along the ferry's stern; you step from it down into
  the well.
- **The bell** hangs at the bow, under an arm on the stem post (8215, 65,
  8297). It is the act: the interaction the `use` trigger fits over the
  bell's cell is the only thing a click there meets, and ringing it plays the
  bell's own sound. It can be rung only from the well.
- **The far jetty** (x 8248–8259) is where the ferry puts you down
  (8252, 64, 8298), its own ferry moored beside you.
- **The Thing**, about seventy blocks beyond the bow, stands on the sea floor (piece
  origin 8170, 54, 8198) and rises 96 blocks from it: waist-deep in the sea,
  an octopus mantle bent forward onto hunched shoulders with no neck, a beard
  of feelers hanging over the chest, long narrow bat-like wings raised behind,
  its east claw raised and its west claw gripping the water, and two slanted
  eyes of ochre froglight. It is built for one side only — the one its camera
  sees; the form's box ends behind it, and that face is its flat back.

Both jetties and the slip carry `atmosphere/sea-fog` from the first tick: fog
from the eye to 32 blocks, the sky and the clouds under it too. From anywhere a
body can stand, the Thing is far inside the fog.

## The cutscene

Ring the bell. The ferry's link (one repeatable `use` trigger) plays one
`sequence`; the cutscene is `party: present`, so **every player in play is
shown by a stand-in where they stood** — a mannequin wearing their own skin,
armour and held items, facing as they faced — and the wide shot shows them in
the boat.

| tick | what happens |
|---|---|
| 0 | the bell sounds; the volume round every camera pose (x 8162–8270, y 24–104, z 8198–8398) is painted `atmosphere/sea-fog`; each player leaves a stand-in and the camera cuts to low behind the ferry's stern (8215.5, 66.5, 8306.5), the party's heads in the bottom of the frame |
| 0–120 | **shot 1**, six seconds: the camera rises diagonally up and forward over the boat toward the Thing, to a close-up under its face (8215.5, 72.5, 8262.5, 40 blocks from it) |
| 120 | **a bolt strikes the sea beside the figure's raised wing** (8268, 63, 8196), and in the same tick the volume holding the ferry, the Thing's front and the whole of shot 2 (x 8166–8266, y 28–100, z 8218–8378) is painted `atmosphere/clearing`: the fog leaves the camera and the close-up stands in the flash |
| 121–281 | **shot 2**, eight seconds: from the close-up the camera pulls back and up, away from the Thing, to high behind the ferry (8231.5, 86.5, 8345.5), widening until the boat with the party's stand-ins in it and the whole figure share the frame. Both shots aim at one point on the face, so the cut between them keeps the aim |
| 282 | the camera returns everyone to where the ringer stood — in the well, since the bell is reached from nowhere else; the stand-ins leave unseen; the clearing is painted `atmosphere/sea-fog` again |
| 283 | whoever is in the well is carried to the far jetty; `flag/seen` is set |

**It plays once.** Every step of the reveal is guarded on `forbids
flag/seen`, and the flag is set with the carry. A later ring — a player who
stayed on the jetty, boarding afterwards — plays no cutscene: the bell sounds,
whoever is in the well is blinded for fifteen seconds, told *the ferry slides
out into the fog*, and carried.

**There is no fog-edge return.** `world.boundary.returns` is `false`: the
build proves no body can walk out of the region or into the open sea, so
nothing pulls a creator back who flies out with `/trigger dw.free` to look at
the far views.

## The clearing, measured

The owner asked for the wide shot to show the boat and the Thing in a clearing
ringed by fog. Fog in the pinned client is a property of **the camera**, not of
the space it looks through: every frame the client samples the atmosphere in a
Gaussian kernel of 4-block cells round the camera, and draws distance fog from
the camera out by the fog start and end that sample gives. So what the clearing
can be is decided by two things, and both were read through the client's own
classes (`measure/FogEdge.java`, run by `measure/clearing.sh` over the camera's
emitted keyframes, `measure/keyframes.txt`; readings in
`measure/clearing-readings.txt`) — the same `GaussianSampler`,
`SpatialAttributeInterpolator` and `EnvironmentAttributeMap` calls, and the same
`AtmosphericFogEnvironment.setupFog` rain offset transcribed from its bytecode,
that this level's first fog measurement used.

1. **The camera stands wholly in the clearing for the whole of shot 2.** At
   every keyframe from tick 121 to the last, the repainted cells carry
   1.000000000000 of the kernel: the client reads the clearing's fog and
   nothing else, and the cut at tick 120 lands in one client tick, as the
   repaint did when this level first measured it.
2. **The ring is the clearing's fog distance round the camera.**
   `atmosphere/clearing` keeps sea-fog's colours and precipitation (a change
   of precipitation would ease the cut over a second) and sets fog 320/476,
   which the storm's rain offset makes **effective 160 → 220 blocks**. At the
   wide shot's pose:

| from (8231.5, 86.5, 8345.5) | distance | fog |
|---|---|---|
| a stand-in in the well | 53 | 0.000 |
| the face | 124 | 0.000 |
| the top of the raised wing | 146 | 0.000 |
| the west wing tip | 150 | 0.000 |
| the raised claw | 140 | 0.000 |
| the sea beyond the figure (8215, 63, 8160) | 188 | 0.462 |

   Everything in the frame is clear, and the sea fades into fog from 160
   blocks out — which is also where the pinned view distance (ten chunks)
   ends the world. That is the ring the wide shot shows.

**What the client cannot show is the painted edge itself.** The sea just
outside the painted volume, 46 blocks behind the camera (8231, 63, 8385), reads
**0.000** fog: a cell's atmosphere fogs only a camera that stands in it, never a
camera looking at it, so the boundary of the repainted box is not drawn. The
box still decides everything that matters — it is what the camera samples —
and the sea around it stays painted sea-fog, which any camera that leaves the
clearing (a creator's free camera) meets at once. The figure's top and its
back stand outside the painted box, which changes nothing a camera in the
clearing sees.

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

## The key frames

`review/keyframe-t000.png`, `-t051`, `-t121`, `-t172` and `-t272` are the
camera at ticks 0, 51, 121 (the close-up, as the bolt strikes), 172 and 272
(the wide shot), each posed exactly as the emitted keyframe in
`measure/keyframes.txt`, fov 70, drawn by `delvec snapshot` — the CPU draft
renderer, which draws blocks only: **no fog, no bolt, no entities, so no
stand-ins and no bell**, and a pale slab under the figure where it draws the
sea floor of the figure's box. They show the composition: the stern rail and
the stem post in the foreground of the first frame, the face filling the
close-up, and in the wide shot the ferry at the bottom of the frame between
the near jetty and the strait with the whole figure above it. What the frames
cannot show is looked at in a real client.

## What to look for

Serve it with the engine's playtest server, from the engine branch
`feat/the-thing-beyond-the-fog` (neither the verb nor the stand-ins are in a
released engine), and look at it in a real client — the fog, the bolt and the
stand-ins are client-side and no render here can show them.

1. **You arrive on the near jetty** (8205, 64, 8299) in fog and rain under a
   thunderstorm. Nothing beyond about thirty blocks is visible.
2. **Choose the passenger's kit, walk through the gap in the east rail and
   along the pier, and step down into the ferry's well** — *Board the ferry*
   completes as you step in. **Ring the bell at the bow.** Look for: the bell
   reading as the thing to use, without the hint.
3. **Shot 1** (six seconds): the camera starts low behind the stern, the
   party's stand-ins in front of it, and rises over them and the bow toward
   the north. Look for: **the stand-ins reading as the party** — your own
   skin, your armour and what you hold, standing where you stood and facing
   as you faced.
4. **The bolt and the close-up.** Look for: the bolt, the sky flash and the
   thunder arriving with the fog cut away; whether the face reads at first
   sight.
5. **Shot 2** (eight seconds): the camera pulls back and up until the ferry,
   with the party in it, and the whole figure share the frame. Look for: the
   two of them in one frame; the sea fading to fog round them; the pull-back
   being smooth from the close-up with no jump in aim.
6. **The camera returns; you are on the far jetty** (8252, 64, 8298) —
   *Cross the strait*, and the delve completes. Look for: one or two frames
   of the ferry's well between the camera's return and the carry.
7. **With a second player** anywhere — on the jetty, on the pier: both are
   shown by stand-ins where they stood, watch the cutscene, are put down in
   the well where the ringer stood, and are carried together.
8. **Ring the bell a second time** (a fresh join after the crossing, boarding
   from the jetty): no cutscene — the bell, fifteen seconds of blindness,
   *The ferry slides out into the fog.*, then the far jetty.
9. **Fly out with `/trigger dw.free`** and look at the figure from anywhere:
   nothing returns you; `/trigger dw.free` again puts you back in your body.

## What the compile says

On the engine branch (delvec 1.8.1):

    stand-in binding: 1 cutscene(s) examined, 1 present (stand-ins placed and removed), 0 absent (none placed)
    lightning binding: 1 strike(s) declared, 1 struck block(s) read, 1 post(s) within reach examined, 0 refused
    boundary binding: the region does not return; 4 place(s) a body is put examined, 0 outside; 378 reachable cell(s) examined for a way out; 0 refused
    link gathering binding: 1 link(s) carried after their root's cutscene, 0 press cell(s) outside their volumes over 378 walk cell(s)
    DW0311 binding: 4 leg(s); 3 walked, 0 carried by a crossing, 1 carried by a link, 0 carried by a loop; 1 link(s) declared, 1 live on some leg, 1 taken; 0 gather(s) declared
    DW0921 binding: 1 quest configuration(s), 19 route cell(s), 392 cell(s) a body can reach by walking, falling, jumping or swimming (14 of them afloat), 0 it cannot leave; 0 link stand cell(s) served as a way out

The camera's clip check (`DW0308`) and angular budget (`DW0347`) pass on both
shots: the climb passes 0.7 of a block over the stem post's arm and 1.7 over the party's heads, and the
aim turns 7° across shot 1 and about 22° across shot 2's eight seconds.

## State

- **Machine ladder** on the `validation/` image (engine `5dca19d9a`, this
  content at `aea21c7`): PackTest **20 of 20 required tests passed**
  (`standin` — a stand-in wears its player's profile, facing and gear — and
  `lightning_0` among them); the mineflayer critical path **passed, 5
  steps** — the bell clickable from 16 of 19 stances, rung from the well,
  `obj/far-shore completed on the landing`, and the run's own entity record
  shows the bot's stand-in removed by the cutscene's end at
  (8215, −128, 8298), the column of the well cell it rang from.
- **Staging gate**: REFUSED on two findings, both the design record the
  level does not carry (`drill3-01`, `drill3-03`): no approved image under
  `design/`. An approved image is the owner's to give; it is not overridden.
- **Looked at by the owner**: the figure reads at first sight, and the carry
  works. Not yet walked: everything in *What to look for* — the stand-ins,
  the re-shot reveal, the clearing and the bell.
