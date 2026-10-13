# The Glasshouse — design record

**What this level is for: it is the engine's standard level for judging renders.** Every change to the render route — tone curve, light, sky, weather, denoise — is judged on this level's showcase pictures. So it is built to look good in a picture, and to hold, each in a place a camera can frame, everything a render can get wrong: open sky over grass, leaves and still water; materials whose tones a viewer knows (oak planks, red brick, pale stone, glass); sky light falling through glass; a room lit only by placed light of several kinds; one dark low place lit by a single source; and a long view to the horizon.

A small delve: 1–4 players, about 12 minutes, one character, no combat. Every later round is judged against this file. The geometric facts in §3 are the authority on size and position; the reference views in `design/reference/` are the authority on look and mood only. Where they disagree, §3 wins.

## 1. The fiction

An old walled kitchen garden stands on an upland shelf above a wide valley. Against its north wall, where the sun reaches all day, is a lean-to conservatory of glass in white frames, and in it an old lemon tree in a tub. Beside the conservatory is the head gardener's brick potting room, and under the potting room is the stove cellar: the stoke-hole whose furnace sends warm air through flues under the conservatory floor.

It is the end of a clear autumn day. The sky is clearing as the sun goes down, which in this valley means one thing: the first frost of the year will come down the valley tonight. Wenna Hale, the head gardener, burnt her palm on the stove door this afternoon and cannot grip a handle. The party are visitors walking the estate at the end of the day; she asks them to shut the conservatory's roof vents and light the stove before the lemon tree freezes. When it is done, she sends them up to the belvedere to watch the sun go — the one thing, she admits, she has never had the time to do at this hour.

Nothing here is hostile. The pressure is the frost, and it never arrives on stage.

## 2. The walk

1. **The lime walk** (arrival). A short gravel avenue between lime trees, rough grass either side, ending at a brick gateway in the garden's east wall with lantern piers. The party arrive with the sun ahead of them, low over the garden wall.
2. **The garden.** Through the gate the whole garden opens: the long reflecting pool on the east–west axis mirrors the gold and rose sky, the conservatory glows against the north wall with the sun shining through it, and the belvedere stands at the far west end against the sunset. Lanterns on short stone posts line the paths. The potting room's lit window draws them to the north-east corner.
3. **The potting room** (quest 1). Wenna, among plank benches, clay pots and seed drawers, lit by a hanging lantern over the bench, candles on the shelf and sill, and a wall torch by the cellar hatch. She explains the frost and asks for the vents.
4. **The conservatory** (quest 2). Back across the garden and in through the glass doors. Inside, sky light falls through the glass roof onto plank staging, ferns and the lemon tree; the vent winding gear is at the east end. Winding it shuts the roof lights.
5. **The stove cellar** (quest 3). Back to the potting room; Wenna hands over the matches and points at the hatch. A narrow stone stair down to a low stone cellar lit by one lantern at the foot of the stair: the coal heap, the iron furnace, flue pipes leading off under the conservatory. The party light the furnace; its glow becomes the room's second light.
6. **The belvedere** (quest 4, finale). Wenna sends them to the west wall. Up the stone steps to the terrace: a balustrade, two urns, a bench, and the valley — level grassland running far west to low hills, the sun on the horizon, the sky deep blue overhead shading to gold and rose. The delve ends there.

## 3. Geometry

The site is one row west to east — belvedere, walled garden, lime walk — with the conservatory and potting room against the garden's north wall. Flat open ground at y 64 (`datum/grade`), inside a low valley surround (`horizon: valley`, ratio 3.0, rim 16) with a boundary of margin 8, so the long view runs over the valley floor to low hills. `view_distance` 16 chunks.

| place | box (play space) | floor | overhead | joined by |
|---|---|---|---|---|
| lime walk | 14 × 8, at [55, 26] (pinned) | y 64 | open 12 | east gate, 3 wide, to the garden |
| garden | 40 × 30, at [14, 15] | y 64 | open 10 | gate; glass door; potting door; terrace steps |
| conservatory | 20 × 10, at [19, 4] | y 64 | 7 of headroom, glass lean-to roof 4 courses | double glass door, 2 wide, to the garden |
| potting room | 10 × 8, at [42, 6] | y 64 | 4 of headroom, tiled roof 3 courses | plank door, 1 wide, to the garden; hatch stair down |
| stove cellar | 8 × 6, at [42, 6] | y 59 | 4 of headroom | stone stair, 2 wide, up through the potting room floor |
| belvedere | 8 × 8, at [5, 26] | y 69 | open 6 | stone steps, 3 wide, hosted in the garden against its west wall |

Inside the garden: the reflecting pool, 18 × 5 of still water edged in pale stone, centred on the long axis; gravel paths round it and to each door; four lawn quarters with clipped hedges; four fruit trees in leaf; lanterns on stone posts along the paths. The lime walk carries six to eight lime trees. Region 72 × 32 × 52 from [0, 54, 0].

## 4. Light, designed with the rooms

- **Outdoors** is lit by the sky, with placed light designed in: lantern posts along the garden paths, lanterns on the gate piers, and the conservatory and potting room windows glowing from inside. At night the garden still reads by these.
- **The conservatory** is lit by the sky through glass. A pair of lanterns hangs from the ridge for the night.
- **The potting room** is lit only by placed light of three kinds: a hanging lantern over the bench, candles on the shelf and window sill, and a wall torch by the cellar hatch.
- **The stove cellar** has one light: a lantern at the foot of the stair. Lighting the furnace adds the second.

## 5. The hour

`time` `{"sun": "setting", "phase": "waxing-crescent"}`, `weather` `clear`. The sun stands on the western horizon: it lights the garden low and gold from the belvedere end, shines through the conservatory's glass, and stands in the long view. The clear sky is also the fiction: a clearing sky at sundown is what brings the frost. The build's clock line reads day 5, daytime 12782.

## 6. The render items and their cameras

Each camera is placed at step 8b; the render round re-shoots each under clear sunrise, noon, sunset, night, rain and thunder.

| render item | where | camera |
|---|---|---|
| open sky: grass, trees, path, still water showing the sky | garden, from inside the east gate looking west along the pool | `garden-pool` |
| known material tones: oak planks, red brick, pale stone, glass | the garden's north side: the potting room's brick front and plank door, the stone path and pool edge, the conservatory's glass front | `north-front` |
| sky light falling inside under glass | conservatory interior, looking along the staging to the lemon tree under the glass roof | `under-glass` |
| a room lit only by placed light, of at least two kinds | potting room interior: lantern, candles, torch | `potting-room` |
| a dark low place lit by one source | stove cellar from the stair foot, the lantern and the furnace | `stoke-hole` |
| a long view: distance and the sky at the horizon | belvedere, looking west over the balustrade | `long-view` |
| the whole map | high to the south-east, looking north-west and down | `whole-site` |

## 7. Cast and classes

- **Wenna Hale**, head gardener, in the potting room throughout. A player body in her own skin (an older woman in a gardener's apron).
- **Classes**: Visitor (coat and apples) and Garden Apprentice (secateurs and bread). No combat; the kits are flavour.

## 8. What the released engine is asked for

Nothing this design needs is outside `delvec 1.13.0`. The pool is contained still water drawn by the garden's own piece at step 9, off the walked route; the furnace's light is a `set-block` of a lit furnace at the quest beat.
