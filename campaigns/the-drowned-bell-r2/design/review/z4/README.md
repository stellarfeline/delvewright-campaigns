# Z4 礼拜堂中庭 — Chapel Ward, review set

What each camera answers. The zone is a roofless four-range cloister on the upper
shelf: outer range wall, a three-wide walk, an arcade screen, and the garth in the
middle, with the hour-vault under it.

Reproduce every image here:

```sh
# engine at the pin `zone-audit.yml` carries in GRAMMAR_REF
cargo build -p delvewright-grammar --bin delve-grammar --release
delve-grammar expand --file design/programs/z4-chapel-ward.json \
    --region 27x12x33 --seed 1 --id z4-chapel-ward -o out/
delve-render piece out/z4-chapel-ward.nbt -o shots/ --size 900 \
    --textures <the pinned 1.21.11 client jar>
```

**The renderer has no author-aimed camera.** An interior shot is aimed by a
declared anchor: a position and a cardinal facing. Eight of the shots below are
aimed by **review standpoints** — anchors with no content behind them, added to a
scratch copy of the expansion's metadata before rendering and listed in
`standpoints.json`. Nothing was added to the program, and the shipped
`prefabs/z4-chapel-ward.json` does not carry them. Add them back with:

```sh
python3 - <<'PY'
import json
m = json.load(open("out/z4-chapel-ward.json"))
for name, s in json.load(open("standpoints.json")).items():
    m["anchors"]["anchor/" + name] = s
json.dump(m, open("out/z4-chapel-ward.json", "w"), indent=2)
PY
```

## The exterior and the plan

| shot | the question it answers |
|---|---|
| `top.png` | is this a cloister? The four ranges, the arcade ring, the garth, the oculus grate and the crypt stairwell in the paving, the canopy in the north-west |
| `ext-nw.png` | the silhouette from the way on: a walled enclosure on the rock shelf, broken along the top, with the banded door in the south face |
| `ext-se.png` | the same from the drowned ward's side — the face the player sees from below |

## Inside, at a body's height

| shot | standpoint | the question it answers |
|---|---|---|
| `eye-look-terrace.png` | 13,8,3 south | **beat 4.1** — the whole cloister from the head of the north flight, three courses up. Arcade, plinths, oculus, canopy in one frame |
| `eye-look-cloister.png` | 13,5,21 north | **beat 4.1** — the garth from its middle, looking at the north arcade and the way on beyond it |
| `eye-look-arcade-in.png` | 6,5,16 east | **beat 4.1** — does the screen read as an arcade from inside the garth, or as a wall with holes |
| `eye-look-walk-west.png` | 2,5,22 north | **beat 4.2** — the west walk: the heaps against the range wall, the fallen lying in them, and the way past |
| `eye-ward.png` | `anchor/ward` | **beat 4.3** — the ground the Two Sextons are fought on, from the middle of it |
| `eye-canopy.png` | `anchor/canopy` | **beat 4.3** — the collapsed canopy as cover: what the fight has to move around |
| `eye-station-1.png` | `anchor/station-1` | **beats 4.4, 4.5** — a station of the hour-round. The three plinths are the only chiselled stone in the zone |
| `eye-look-door.png` | 13,5,28 south | **beat 4.6** — S3: oak, iron-banded, a ring handle on each leaf, in its arch over the chapel step |
| `eye-look-gap.png` | 19,5,28 south | **beat 4.6** — the broken bay beside it, and the tracery the ward below is seen through |
| `eye-look-crypt.png` | 13,2,21 north | **beat 4.5** — the foot of the crypt stair and the barred gate the rite opens |
| `eye-look-vault.png` | 13,1,12 north | **beat 4.5** — inside the hour-vault: the pier ranks and the wall the hours are cut into |
| `eye-hour-1.png` | `anchor/hour-1` | **beat 4.5** — one of the seven hour recesses, from the cell a reading stands in |

## What the images cannot show

- `eye-look-vault.png` and `eye-hour-1.png` are of a room a player only reaches
  after the rite. The renderer draws the piece as built, bars standing.
- The three plinths are two courses tall and are deliberately not climbable, so
  the reachability measurement reports two of their tops as unreachable floor
  open to the sky. That is the plinth being a plinth.
- Every anchor facing north or south at the piece's own outer face — `way-on`,
  `stoop` — renders as an empty frame, because what those anchors are about is
  the zone on the other side of the seam.

`shots.json` is the renderer's own manifest: every camera, its position and what
it was aimed at.
