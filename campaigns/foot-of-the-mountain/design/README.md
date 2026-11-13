# Festival Day in Kelderby — approved design

The approved reference set for this campaign: the salvage ground's reference, drawn over a path-traced picture of the built town from the sea, and four views of the whole map anchored on it. Author from the image, judge against it, present every choice beside it.

`reference/salvage-ground` was drawn from its prompt over the base picture alone; every later view was drawn chained on its interaction under one style contract (`style.txt`). Each image's request, prompt, frame and anchor is in the sidecar beside it.

| image | what it shows | hour |
|---|---|---|
| `reference/salvage-ground` | The whole island town from the sea, and out in front of the quay, past a band of open deep water, the salvage ground: low wide sandbars joined into one irregular shallow patch, pale turquoise shallows shading to deep blue, a curving broken outer bar, six barrels afloat in the channels. The style anchor for the series. | early morning (daytime 1000), clear |
| `reference/from-the-castle` | The town from the castle gate on the summit in mid-morning: the castle road below, the square with the festival stage, the main street down to the quay, the lighthouse, the salvage ground out at sea. | mid-morning (daytime 4000), clear |
| `reference/plan` | The island as a straight-down plan at noon: the castle on its mountain, the road down to the square and stage, the main street to the quay, farms, pens and orchards on the flanks, the lighthouse, and the salvage ground offshore. A plan of the design's parts, not of the built streets. | noon (daytime 6000), clear |
| `reference/harbour-at-dusk` | The harbour at sunset from the water off the quay: the raiders' longboats rowing in, townsfolk with torches on the quay, the lighthouse lamp lit, the town's windows and lanterns coming on. | dusk (daytime 12000), clear |
| `reference/festival-night` | The cathedral square at night: the town gathered round the stage, bunting and hanging lanterns across the streets, lit windows, a lavish firework show over the square and the dark sea beyond. | midnight (daytime 18000), clear |

The salvage ground is built to `reference/salvage-ground` with its water opened up for a boat: the reference's sandbars are larger than the play needs, so the built bars keep its look and leave wide channels. The showcase cameras that answer each image are in `cameras.json`; the camera answering the salvage ground frames the town, with the salvage ground in the foreground rather than whole.

## Answers on the design

- The four map views record the town's look and mood; every position comes from the map. The salvage ground is built to `reference/salvage-ground` alone: the shoals' place in `reference/from-the-castle` and the islets in `reference/plan` are not the design.
- The salvage ground as built (content `dd816557`, seen from the sea at the reference's pose and from its showcase camera) is accepted as it is: its shape is not changed further.
- The salvage ground: built to its reference, offshore past open deep water, low wide sandbars joined into one irregular shallow patch, water shading from pale turquoise to deep blue, a curving broken outer bar, barrels floating in the channels. The final establishing shot frames the town; it need not take in the whole salvage ground (the town would read too far away).
- The salvage area is about nine times the cove's first one (about three times as wide and long), set farther from the shore, with a few drowned in it for challenge.
- The shoals are obstacles only. The crates are barrels standing one block above the water, touching its surface. The player never leaves the boat: they row round the shoals and open each barrel from the boat. Counting is per barrel opened.
- The rectangular bay piece is removed; the natural bay of the coast stays as it was, and the cargo task is authored in it. The water rendering is not at fault.
- The sea establishing shot reads well. Final pictures are rendered at a higher resolution (3840×2160), because a detailed picture will be zoomed into; the town is shown finished, with no look before everything is done.
- Lamps on the playable hillside are right and stay.
- The fair field's stepped edge seen from the sea, and the castle's slope, are accepted as they are.
- The ground's bare patches never use dirt-looking blocks: gravel, stone, andesite, tuff, sand and the like.
