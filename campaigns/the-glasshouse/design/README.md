# The Glasshouse — approved design

This set is the approved design. Author from the image, judge against it, present every choice beside it.

The images are the authority on look and mood. The geometric facts in `../DESIGN.md` §3 are the authority on size and position; where an image and §3 disagree, §3 wins. Every image is drawn under the declared hour, `sun: setting`, `clear` (its row in `../design.json`).

Provider `gemini-native`, model `gemini-3.1-flash-image`. One style contract (`reference/style.txt`, sent as `--style-note`) for every image. View 1 was drawn from its prompt alone; every other image is chained on view 1's interaction (`request.chain_from` in its sidecar), never on another image.

| image | what it shows |
|---|---|
| `reference/view1-garden` | From inside the east gate looking west along the reflecting pool at sunset: the lean-to conservatory against the north wall, the potting room's lit window, fruit trees, lantern posts and the belvedere against the setting sun. The series' style anchor. |
| `reference/view2-plan` | The garden straight down, north up: the walls, the pool on the long axis, paths and hedged quarters, the conservatory and potting room on the north side, the belvedere on the west wall and the lime walk to the east gate. |
| `reference/view3-terrace` | The long view from the belvedere: balustrade, urns and bench in front, level grassland running west to low hills, the sun on the horizon and a crescent moon. |
| `reference/view4-aerial` | The whole site from high to the south-east: the walled garden, the pool catching the sky, the glowing conservatory, the potting room, the belvedere and the lime walk, with grassland to the hills. |
| `concept/arrival-near` | The lime walk at eye height: gravel between lime trees, the brick gateway with lantern piers and an open oak gate, the conservatory roof over the wall. |
| `concept/arrival-far` | The lime walk from above and east: the avenue to the east gate, and the garden, pool and conservatory beyond the wall. |
| `concept/garden-near` | Beside the pool's east end looking west: still water mirroring the sunset, lit lantern posts, hedges, a fruit tree, the conservatory on the right. |
| `concept/garden-far` | The whole garden from the south-east corner of the wall: pool, lawn quarters, fruit trees, lantern posts, the conservatory and potting room on the north wall, the belvedere against the sunset. |
| `concept/glass-near` | Inside the conservatory: low sun through the glass front onto plank staging and a tiled floor, the lemon tree in its tub, the vent winding wheel on the brick back wall, sky through the glass roof. |
| `concept/glass-far` | The conservatory front square-on from the lawn: glass front and roof in white frames on a brick plinth, the double door and path, the potting room at the right edge. |
| `concept/potting-near` | Inside the potting room: plank floor and benches, pots and seed drawers, a hanging lantern, candles on shelf and sill, a wall torch, the cellar hatch, and Wenna with her bandaged hand. |
| `concept/potting-far` | The potting room from the garden's north-east corner at the end of sunset: brick walls, the door ajar spilling lamplight, a glowing window, lit lantern posts. |
| `concept/cellar-near` | The stove cellar from the stair foot: one wall lantern the only light, the furnace with its fire just lit, coal heap and shovel, flue pipes. |
| `concept/cellar-far` | A cutaway: the lit potting room above, the stair down through its floor, the stone cellar below with one lantern and the glowing furnace. |
| `concept/terrace-near` | On the belvedere looking west: balustrade, urns and bench, grassland to the far hills, the sun on the horizon, a crescent moon. |
| `concept/terrace-far` | The garden's west wall from the grassland outside: the belvedere standing out from it, figures at the balustrade, the conservatory roof behind. |

Known drift from §3, not to be built: the plan and aerial views stand the conservatory inside the walls rather than in the north wall line; the garden far view shows more than four fruit trees; the belvedere far view puts the sun behind the garden. `concept/potting-far` and `concept/cellar-far` read slightly later than sunset; their sky is the declared one.
