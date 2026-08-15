# The composed map — review set

Six named views of Halgrave composed as one program, plus the shot manifest that
records the camera of each.

**What these images are of, and it is not `map.json`.** The map program is red on
six contract gates, and a red expansion writes no prefab, so there is nothing of
`map.json` to render. These views are of a **massing variant** of the same site
plan, at the same region and seed, with Z1, Z2 and Z4 left as solid masses
instead of composed. Those three are the only zones whose programs declare a
spatial contract, and dropping them is exactly what makes the composition
contract-free and therefore exportable. The rock, the sea, the curtain, the
apron, the causeway, Z0's shore, Z3's ward, Z5's keep, Z6's cistern and Z7's
tower are all the composed article. The gatehouse front, the cliff road and the
cloister are the three blank masses.

`../../map-composition-log.md` §6 carries the derivation and the numbers.

| image | view | how it was aimed |
|---|---|---|
| `front-elevation.png` | the south face, square on — the view from the flat | `--view name=front-elevation,face=south` |
| `west-elevation.png` | the seaward face, square on | `--view name=west-elevation,face=west` |
| `east-elevation.png` | the low lobe's face, square on | `--view name=east-elevation,face=east` |
| `site-plan.png` | straight down | `--view name=site-plan,face=up` |
| `section-south-north.png` | the south face with the near half cut away | `--view name=section-south-north,face=south,cutaway=true` |
| `aerial-south-west.png` | the three-quarter aerial | `--view name=aerial-south-west,yaw=225,pitch=-32` |

## What the images say, read against `../../reference/map-brief.md`

- **The tower is built and the bell is in it.** The front elevation and the
  aerial show the square tower with a hole of sky through its top storey and the
  oxidised-copper mass of Mercy filling it. That is the campaign's recognition
  feature and it survives at silhouette scale.
- **The site is a ribbon, not a compact stepped mass.** The site plan is the
  clearest statement of it: 79 wide by 436 long, an aspect of 1 : 5.5. The brief
  says in as many words that a layout stringing the zones end to end loses the
  place. The composition does not string them by choice — the zone boxes'
  own depths along the route sum to 350 blocks between the flat and the crown,
  and a `split` partitions, so no packing shortens that chain.
- **The tower does not read as twice the height of anything else.** From the
  wake point to the belfry is 338 blocks and 40 of rise: the crown subtends
  6.7°. The brief derives 27° twice over, by two independent methods 1.9% apart,
  and fixes the standoff at 75.7–77.2 blocks.
- **`section-south-north.png` is byte-identical to `front-elevation.png`.** The
  `cutaway=true` flag is recorded as applied in `shots.json` and cut nothing on
  this subject. On three control subjects the same flag on the same face visibly
  cuts. This is stated rather than explained; `../../map-composition-log.md` §7
  carries the controls.
