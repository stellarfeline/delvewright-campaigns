# The Ferry Landing

The demo level for **a skin wears its second layer** (spec-0097). The skin
toolchain paints the overlay shell: a beard, hair, a hood and a high collar
stand half a pixel off the head and the neck. A mannequin can hide a layer
with `skin.hidden_layers`. A mob's sheet is drawn to that mob's own boxes.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-ferry-landing/

Every skin and mob sheet is composed by the engine's skin toolchain
(`delve_skin`) from `campaigns/the-ferry-landing/skins/cast.json`. No pixel
is painted by hand. The two places, the landing stage and the quay top, are
detailed pieces: `delvec detail` expands `programs/landing.json` and
`programs/quay.json` inside the boxes the site plan hands them, and freezes
them as `prefabs/the-ferry-landing-landing` and
`prefabs/the-ferry-landing-quay`. Everything outside the two boxes comes from
`world-edits.json`. Two scripts write those documents:

    python3 campaigns/the-ferry-landing/design/build_pieces.py
    python3 campaigns/the-ferry-landing/design/build_quay.py
    delvec --prefabs prefabs detail campaigns/the-ferry-landing --all

## What it is

A small stone quay at sundown. The sun is on the western horizon and the
full moon is rising in the east. The last ferry has gone.

- **The landing stage** is a spruce deck on log piles at the foot of the
  quay wall, one block over the water (x 8200–8215, z 8188–8195, walked at
  y 64). It has a rail on its three water sides and lantern posts at the rail.
- **The quay wall** is stone brick, four courses high over the deck, with
  lantern posts standing at its foot.
- **The steps** are a two-wide flight against the wall face. They climb west
  from the deck to a gateway through the wall: two piers and a lintel, with a
  lantern on each pier.
- **The quay top** is paved stone, four blocks above the deck (z 8197–8204,
  walked at y 68). Its edge over the landing is open, with three bollards,
  two of them carrying lanterns, a row of lamp standards a step back from the
  edge, and more along its back. A bench faces the water. At the back stand
  a stone toll house and a timber warehouse, with a grass bank either side.

You arrive on the landing stage (8207, 64, 8191).

### Who stands on the landing

Nine bodies stand on the deck. The ferryman is at the rail; the other eight
stand in a row at z 8192 and face the quay wall, so you see their faces from
the deck and from the quay top above.

| Where | Body | What its second layer carries |
|---|---|---|
| (8209, 64, 8188), at the rail | **Hobb**, the ferryman (mannequin) | a full beard, greying, on the hat shell's chin, mouth and lip rows, its sides and underside |
| (8201, 64, 8192) | a **zombie** (stage-5 actor) | long matted black hair on the zombie's only shell, the hat |
| (8203, 64, 8192) | a **drowned** (stage-5 actor), holding a trident | an outer layer with weed-dark long hair and a high collar, drawn at the outer model's base positions |
| (8205, 64, 8192) | a **villager** (stage-5 actor) | a robe dyed harbour blue on the villager's long robe shell, darker down the front opening and at the hem |
| (8207, 64, 8192) | a **piglin** (stage-5 actor), holding a golden sword | a russet jacket with sleeves to the wrist on the piglin's jacket and sleeve shells, open down the front |
| (8209, 64, 8192) | **Wenna**, a toll-keeper (mannequin) | long auburn hair, **with the hat layer hidden** (`hidden_layers: ["hat"]`) |
| (8211, 64, 8192) | **Morwen**, her twin (mannequin) | the same skin file as Wenna, drawing every layer |
| (8213, 64, 8192) | **the Pilgrim** (mannequin) | a hood over the hat shell, open at the face, falling onto the jacket's shoulders |
| (8215, 64, 8192) | **Mr Quill**, the harbour clerk (mannequin) | a high collar: the jacket shell's top two rows, all the way round |

The four mob sheets replace vanilla's `minecraft:entity/zombie/zombie`,
`minecraft:entity/zombie/drowned_outer_layer`,
`minecraft:entity/villager/type/plains` and `minecraft:entity/piglin/piglin`
for the whole delve, through `world.json` `textures[]`. The villager's sheet
replaces the plains type layer, not the base villager texture, because the
game draws the type layer over the base and the robe is on it. They show only if the player accepts the server's
resource pack. `delvec textures campaigns/the-ferry-landing` writes vanilla's
sheet beside each one.

Text is short. Hobb tells you the last crossing has gone and that you can
wait up on the quay; the journal then says to go up there. Each of the
others has one line when spoken to.

## What to look for

1. **Stand on the deck in front of the row.** Look at Hobb's beard from the
   side: does it stand off the jaw, rather than lying flat on the face?
2. **Look at Wenna and Morwen side by side.** They wear the same sheet.
   Wenna hides her hat layer and Morwen shows it. Does Morwen's hair read as
   a layer standing off her head, and Wenna's as painted flat on it?
3. **Look at the Pilgrim's hood** from the front and from the side. Does it
   frame the face, with the face set back inside it?
4. **Look at Mr Quill's collar.** Does it ring the neck above the coat?
5. **Look at the four mobs.** Is the zombie's hair on its head, and nowhere
   else? Is the drowned's hair on its head and its collar round its neck,
   where its body really is? Is the villager's robe blue from the shoulders
   to the hem, over its folded arms? Is the piglin's jacket on its body and
   its sleeves on its arms, with nothing floating or missing?
6. **Climb the steps** through the gateway onto the quay top. Stand at the
   open edge between the bollards and look down at the row. Do the beard,
   the hair, the hood and the collars still read from above?
7. **Look at the place.** From the deck and from the quay top, does it read
   as a small harbour quay at dusk: a landing stage, a quay wall with steps,
   lamps lit for the evening?

The edge of the quay top over the landing is open. A fall from it is four
blocks onto the deck: it hurts a little and does not kill.

## State

Built with `delvec` 1.10.0 (dsl 0.37.0) from engine revision
`44ace65f10d9ce1497f5c20ba213e6483dac2dbc`. The runs are in `transcripts/`.

- `validate`, `analyze` and `build` exit 0; two builds are identical (151
  files). The route is proven (`DW0311`: 2 legs, 2 walked). No place traps a
  body (`DW0921`: 0 of 250 reachable cells). Both places are detailed (2 of
  2), and their 4 faces answer the plan's 4 seams. Each piece's own light
  probe reads `lit`: 117 measured cells on the landing, 122 on the quay top.
- Every sheet is judged against its own model's boxes: 8 of 8 (4 mannequin
  skins, 4 texture rows), none refused.
- One mannequin summon carries `hidden_layers:["hat"]`: Wenna's.
- The equipment check binds 2 bodies (the drowned's trident, the piglin's
  sword), none refused. Neither item covers a shell.
- PackTest passed: 43 of 43 required tests.
- The mineflayer critical path passed in 4 steps: choose a class, talk to
  Hobb, reach the quay top, complete. All 14 non-player bodies were present
  (5 mannequins, their 5 hitboxes, 4 actors). Its die-retry and death-loop
  stages did not run, because the level declares no combat and no death.
- The staging gate refuses the level with 2 reds of 122 findings (34 bound,
  26 declared uncoverable, 60 inapplicable). Both, `drill3-01` and
  `drill3-03`, are the design record the level does not carry: an approved
  concept picture in `design.json` and a camera answering it. Serving it to a
  person takes the gate's own deliberate override.

Serve it with the engine's playtest server, from the engine tree, naming this
repository's campaign and prefab library:

    tools/creator/playtest-server.sh up <this repository>/campaigns/the-ferry-landing \
      --prefabs <this repository>/prefabs --delvec <delvec 1.10.0, dsl 0.37.0> \
      --stage-anyway "<reason>" --acknowledge-red 2

It is never copied into a singleplayer save.
