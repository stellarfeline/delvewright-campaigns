# The Ferry Landing

The demo level for **a skin wears its second layer** (spec-0097). The skin
toolchain paints the overlay shell: a beard, hair, a hood and a high collar
stand half a pixel off the head and the neck. A mannequin can hide a layer
with `skin.hidden_layers`. A mob's sheet is drawn to that mob's own boxes.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-ferry-landing/

Every skin and mob sheet is composed by the engine's skin toolchain
(`delve_skin`) from `campaigns/the-ferry-landing/skins/cast.json`. No pixel
is painted by hand. Every block comes from `world-edits.json`, which
`campaigns/the-ferry-landing/design/build_quay.py` writes:

    python3 campaigns/the-ferry-landing/design/build_quay.py

## What it is

A small stone quay at sundown. The sun is on the western horizon and the
full moon is rising in the east. The last ferry has gone.

- **The landing stage** is a spruce deck on log piles at the foot of the
  quay wall, one block over the water (x 8200–8215, z 8188–8195, walked at
  y 64). It has a rail on its three water sides and lantern posts at the rail.
- **The quay wall** is stone brick, four courses high over the deck, with
  lanterns hung from timber brackets on its face.
- **The steps** are a two-wide flight against the wall face. They climb west
  from the deck to a gateway through the wall: two piers and a lintel, with a
  lantern on each pier.
- **The quay top** is paved stone, four blocks above the deck (z 8197–8204,
  walked at y 68). Its edge over the landing is open, with three bollards,
  two of them carrying lanterns, and lamp standards along its back. A bench
  faces the water. At the back stand
  a stone toll house and a timber warehouse, with a grass bank either side.

You arrive on the landing stage (8207, 64, 8191).

### Who stands on the landing

Seven bodies stand on the deck. The ferryman is at the rail; the other six
stand in a row at z 8192 and face the quay wall, so you see their faces from
the deck and from the quay top above.

| Where | Body | What its second layer carries |
|---|---|---|
| (8209, 64, 8188), at the rail | **Hobb**, the ferryman (mannequin) | a full beard, greying, on the hat shell's chin, mouth and lip rows, its sides and underside |
| (8208, 64, 8192) | **Wenna**, a toll-keeper (mannequin) | long auburn hair, **with the hat layer hidden** (`hidden_layers: ["hat"]`) |
| (8210, 64, 8192) | **Morwen**, her twin (mannequin) | the same sheet, byte for byte, drawing every layer |
| (8212, 64, 8192) | **the Pilgrim** (mannequin) | a hood over the hat shell, open at the face, falling onto the jacket's shoulders |
| (8214, 64, 8192) | **Mr Quill**, the harbour clerk (mannequin) | a high collar: the jacket shell's top two rows, all the way round |
| (8202, 64, 8192) | a **zombie** (stage-5 actor) | long matted black hair on the zombie's only shell, the hat |
| (8204, 64, 8192) | a **drowned** (stage-5 actor) | an outer layer with weed-dark long hair and a high collar, drawn at the outer model's base positions |

The zombie and drowned sheets replace vanilla's
`minecraft:entity/zombie/zombie` and
`minecraft:entity/zombie/drowned_outer_layer` for the whole delve, through
`world.json` `textures[]`. They show only if the player accepts the server's
resource pack. `delvec textures campaigns/the-ferry-landing` writes vanilla's
sheet beside each one.

Text is short. Hobb tells you the last crossing has gone and that you can
wait up on the quay; the journal then says to go up there. Each of the
others has one line when spoken to.

## What the row asks that this level does not show

The row also asks for **a villager in a recoloured robe** and **a piglin in a
jacket and sleeves**. The skin toolchain dresses only models whose head,
torso and limbs are the player's size. It refuses `villager` and `piglin`
by name and points at `python -m delve_skin parts <model>`, which prints
their boxes so a sheet can be drawn to them by hand. This level paints no
pixel by hand, so neither mob is in it. A vanilla villager or piglin would
show only vanilla's own second layer and would test nothing here.

## What to look for

1. **Stand on the deck in front of the row.** Look at Hobb's beard from the
   side: does it stand off the jaw, rather than lying flat on the face?
2. **Look at Wenna and Morwen side by side.** They wear the same sheet.
   Wenna hides her hat layer and Morwen shows it. Does Morwen's hair read as
   a layer standing off her head, and Wenna's as painted flat on it?
3. **Look at the Pilgrim's hood** from the front and from the side. Does it
   frame the face, with the face set back inside it?
4. **Look at Mr Quill's collar.** Does it ring the neck above the coat?
5. **Look at the zombie and the drowned.** Is the zombie's hair on its head,
   and nowhere else? Is the drowned's hair on its head and its collar round
   its neck, where its body really is, and not floating or missing?
6. **Climb the steps** through the gateway onto the quay top. Stand at the
   open edge between the bollards and look down at the row. Do the beard,
   the hair, the hood and the collars still read from above?
7. **Look at the place.** From the deck and from the quay top, does it read
   as a small harbour quay at dusk: a landing stage, a quay wall with steps,
   lamps lit for the evening?

The edge of the quay top over the landing is open. A fall from it is four
blocks onto the deck: it hurts a little and does not kill.

## State

Built with `delvec` 1.8.2 (dsl 0.35.1) from the engine branch
`feat/a-skin-wears-its-second-layer`, which is not yet released. The runs
are in `transcripts/`.

- `validate`, `analyze` and `build` exit 0. The route is proven
  (`DW0311`: 2 legs, 2 walked). No place traps a body (`DW0921`: 0 of 253
  reachable cells). Every walkable cell is lit to 7 by the level's own
  lamps. The blockout battery proves both seams.
- One mannequin summon carries `hidden_layers:["hat"]`: Wenna's.
- PackTest passed: 33 of 33 required tests.
- The mineflayer critical path passed in 4 steps: choose a class, talk to
  Hobb, reach the quay top, complete. Its die-retry and death-loop stages did
  not run, because the level declares no combat and no death.
- The staging gate refuses the level with 4 reds of 122 findings (30 bound,
  25 declared uncoverable, 63 out of stage). Two, `drill3-01` and
  `drill3-03`, are the design record a demo level does not carry. Two more,
  `bell-11` and `doune-04`, count objects their checks do not judge: the
  level's one trigger fires on approach, not on a press, and its two actors
  wear nothing, on purpose, because a helmet would cover the hat shell.
  Serving it to a person takes the gate's own deliberate override, which is
  the owner's call.

Serve it with the engine's playtest server:

    tools/creator/playtest-server.sh up campaigns/the-ferry-landing --prefabs prefabs

It is never copied into a singleplayer save.
