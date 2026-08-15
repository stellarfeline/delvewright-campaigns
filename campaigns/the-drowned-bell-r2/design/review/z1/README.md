# Z1 崖道 — review set

Judged against `../../concept/z1-cliff-road.jpg`.

**A cliff section is solid rock with a groove in it.** Four fifths of this piece
is the cliff, the road is one block wide, and its seaward face is a cut plane
where the surrounding rock continues in the assembled world. So every exterior
camera photographs a slab, and none of them can tell you the road is there. The
set below leads with eye-level views from the road, which is the only place a
body ever stands.

| image | camera | what it is for |
|---|---|---|
| `eye-niche_watch_1.png` | on the road at 5,13,4, facing north | the concept's own composition: wall close on the right hand, open drop on the left, the ledge running away ahead |
| `eye-niche_watch_3.png` | on the road at 5,13,21, facing north | the same walk mid-traverse, with 21 open cells ahead — how long the road reads |
| `eye-niche_watch_5.png` | on the road at 5,13,36, facing north | the last stretch, and a recess mouth beside the walking line |
| `eye-niche_5.png` | standing back in a recess at 6,13,32, facing west | what the road looks like from inside the one shelter it offers |
| `corpse-niches.png` | aimed, yaw 250 pitch −8 on `anchor/niche-2`, zoom 0.10 | the two skulls in the wall, at a distance where both are in one frame |
| `sea-front.png` | aimed, square-on at the west face | the seaward elevation — and the honest picture of what this piece does *not* do: the ledge is a seam in a flat plane, not an overhang |
| `road-section.png` | aimed, square-on at the north face | the profile: twelve courses of drop, the ledge, fifteen courses of wall above it |
| `ext-nw.png`, `ext-se.png` | planned exterior three-quarters | massing only |
| `top.png` | planned plan cutaway | plan only |

`shots.json` is the authority on every camera: kind, yaw, pitch, field of view,
and for each eye shot the cell the body stands in and how many open cells lie
ahead of it.

**Two anchors have no eye shot, and that is the design.** `anchor/niche-2` and
`anchor/niche-3` are the corpse recesses — one block wide and one course high
under the niche band, so no body fits in front of them. The renderer says so
(`DW0727`) rather than taking a shot that would show a wall. `corpse-niches.png`
is the aimed camera that answers what they hold.

## Reproducing the set

```sh
delve-grammar expand --file design/programs/z1-cliff-road.json \
    --region 10x28x44 --seed 1 --traversable --reachable-floor \
    --id z1-cliff-road -o out/
delve-render piece out/z1-cliff-road.nbt -o shots/ --size 720 \
    --view name=sea-front,face=west \
    --view name=road-section,face=north \
    --view name=corpse-niches,yaw=250,pitch=-8,of=anchor/niche-2,zoom=0.10
```

The region is the zone's own: 10 x 28 x 44, seed 1. Both of the zone's tuned
values live in the program's `params`, so no `--param` is needed and the
metadata's program hash covers them.

Every standpoint here is a **campaign anchor the program declares**. Nothing was
added to the metadata to take these pictures.

## What the renders cannot show

The road is roofless and the drop is open, so both sides of the frame end at the
edge of the piece and read as flat background. In the assembled world that is
sea, sky and fog on one hand and the cliff continuing on the other — the concept
image's whole atmosphere lives there and none of it is in these bytes. Judge the
road's width, its exposure, the recesses and the stone here; judge the view off
the edge once the zone stands in its surround.
