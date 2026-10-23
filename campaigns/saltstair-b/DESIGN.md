# Saltstair, cut B — design record

**The authority is `campaigns/hillside/DESIGN.md`**: §2 (the peninsula), §3 (the town in words, the eight buildings, the materials, light), §4 (every coordinate, floor and roof), §5.2 (cut B, with its restated junction) and §6 (the judging set: six cameras, the walk, five numbers). This file restates none of it; it records only what that design leaves to the campaign that builds cut B, and every later round of this campaign is judged against both together.

## What this campaign adds

| Decision | Value |
|---|---|
| Campaign | `saltstair-b`, a demo level (`world.json` `demo_level: true`) |
| Heightmap | `terrain/peninsula.png`, a byte copy of `campaigns/hillside/terrain/peninsula.png` (written by `campaigns/hillside/terrain/peninsula.py`) |
| The hour | `time: dusk`, `weather: clear` — the design's "late afternoon" has no clock of its own; `dusk` (12000, the sun low in the west) is the nearest the engine states |
| Horizon | `ocean`, ground music silent (`audio/background_music: {}`), `boundary` margin 8 |
| Cast | none — the design makes a cast optional, and this cut has none |

## Beats

| # | Beat | Place | What happens |
|---|---|---|---|
| 1 | Arrival | `node/upper-town`, on the square | The party appears on the square between the chapel and the inn, the street falling away south to the sea |
| 2 | The quay | `node/lower-town`, on the quay | The party reaches the quay at the foot of the street; the one objective completes and the delve ends |

One quest, one objective (reach the quay), mandatory. No branch, no ending table: one ending, the quay.
