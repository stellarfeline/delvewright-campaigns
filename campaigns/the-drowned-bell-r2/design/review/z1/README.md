# Z1 崖道 — Cliff Road, review set

What each camera answers. The zone is one cut ledge across the seaward cliff: a
shore landing at the south end, a flight climbing five courses onto the road, a
single-file ledge with a bracket line driven into its inner wall, a rock nose the
road goes *through* by way of a rope store with a mouth at each end, and the
gatehouse's own outer wall with a breach in it at the north end. The shelf in
front of the store has gone into the sea, and that gap is the only place on the
road with no floor.

Reproduce every image here:

```sh
# engine at the pin `zone-audit.yml` carries in GRAMMAR_REF
cargo build -p delvewright-grammar --bin delve-grammar --release
delve-grammar expand --file design/programs/z1-cliff-road.json \
    --region 16x24x72 --seed 1 --id z1-cliff-road -o out/
cargo build --release --manifest-path crates/render/Cargo.toml
delve-render piece out/z1-cliff-road.json -o shots/ --size 900 \
    --textures <the pinned 1.21.11 client jar>
```

The region and seed are the ones `programs/zones.json` declares, and every tuned
value lives in the program's own `params`, so no `--param` and no `--role` is
part of the recipe. The zone is past the 48-per-axis structure-template cap on
its long axis, so it ships as a **tile set and one manifest**; `delve-render`
takes the manifest and assembles the tiles into one scene.

**The renderer has no author-aimed camera.** An interior shot is aimed by a
declared anchor: a position and a cardinal facing, and nothing else. Three of the
shots below are aimed by **review standpoints** — anchors with no content behind
them, added to a scratch copy of the expansion's metadata before rendering and
listed in `standpoints.json`. Nothing was added to the program, and the shipped
`prefabs/z1-cliff-road.json` does not carry them. Add them back with:

```sh
python3 - <<'PY'
import json
m = json.load(open("out/z1-cliff-road.json"))
for name, s in json.load(open("standpoints.json")).items():
    m["anchors"]["anchor/" + name] = s
json.dump(m, open("out/z1-cliff-road.json", "w"), indent=2)
PY
```

## The face, and the plan

The west elevation is this zone's own face, and it is the one view the previous
production of Z1 could not produce: it rendered as a flat plane with a seam.

| shot | camera | the question it answers |
|---|---|---|
| `ext-nw.png` | orbit, yaw 315, pitch 30 | does it read as a road? The cut line runs the whole face, the deck's lip throws a shadow along its own undercut, the bracket line is a row of warm points along it, the flight steps down to the shore shelf at the right, and the gatehouse's pale masonry closes the left end |
| `ext-sw.png` | orbit, yaw 225, pitch 30 | the same face from the arrival end: the road as one horizontal line climbing away, with the rock teeth standing out of the drop below it |
| `ext-se.png` | orbit, yaw 135, pitch 30 | the landward back. Massing only: it is the inside of a cliff, and the only thing on it is the gatehouse wall at the far end |
| `top.png` | plan, cutaway | how little of this region is road. The piece is a cliff with a groove cut in it, and the plan is what says so |

## The walk, in travel order

Every camera is at a cell a body stands in, at eye height 1.62, aimed by the
anchor's own facing.

| shot | standpoint | the question it answers |
|---|---|---|
| `eye-shore_foot.png` | `anchor/shore-foot` at 5,8,69 facing north | the arrival. Three cells of shelf where the flat ends, the cliff going up, and the way on rising away in front |
| `eye-shover.png` | `anchor/shover` at 6,13,51 facing north | **beat 1.1.** The whole composition of the concept image: wall close on the right hand, nothing at all on the left, one body's width between them, and the road running away to the lit stone at its end |
| `eye-shover_watch.png` | `anchor/shover-watch` at 6,13,55 facing north | the contested ground seen from four cells up-path — what a player has to fight on, and how little room there is to give |
| `eye-recess_look.png` | standpoint at 6,13,56 facing east | the inner wall from the walking line, and the recess mouth as the notch at the bottom of it. **This is also the shot that shows why there is no better one**: a recess one cell deep off a lane one cell wide is half a block from the camera, so no standpoint in this piece can frame it. The measurement answers it instead — three recesses, six standable cells, all out of the walk |
| `eye-warn_watch.png` | `anchor/warn-watch` at 6,13,48 facing north | **beat 1.2 and the tell of 1.3.** Down the warning run: the brackets along this stretch hang bent, and past them there is no bracket at all |
| `eye-gap_brink.png` | `anchor/gap-brink` at 6,13,28 facing north | **beat 1.3.** The last cell with floor under it. The road simply stops, the drop is open ahead, and the gatehouse wall stands at the far end of a stretch there is no way to walk |
| `eye-gap_back.png` | standpoint at 6,13,17 facing south | the same gap from the far side: ten cells of missing shelf, the inner wall standing over it, and the teeth in the drop below |
| `eye-store_inside.png` | standpoint at 9,13,26 facing north | **beat 1.5.** Inside the rock: the store running through the nose, widening at the middle where the rope is kept, and daylight at the far mouth |
| `eye-rope.png` | `anchor/rope` at 11,13,22 facing north | the cell the Z1 rope binds to, against the timber rack, with the length of the store beside it |
| `eye-store_out.png` | `anchor/store-out` at 6,13,16 facing north | coming out of the lower mouth: the ledge resumes, the bracket line resumes with it, and the gate is now the thing at the end of the road |
| `eye-breach.png` | `anchor/breach` at 5,13,2 facing north | **beat 1.6.** Standing in the breach itself: dressed masonry two cells thick with a hole broken through it, and nothing beyond but the next zone |

## What the renders cannot show

Everything off the seaward edge. The road is roofless and the drop is open, so
the left of every frame ends at the edge of the piece and reads as flat
background — in the assembled world that is sea, surf, fog and sky, and the
concept image's whole atmosphere lives there. **Judge the road's width, its
exposure, the lip, the bracket line, the gap and the stone here; judge the view
off the edge once the zone stands in its surround.**

The other thing they cannot show is the sea itself. This piece places no water:
the tide is one moving plane the assembled world carries (`../../tide.md`), and a
basin of water inside a piece open on three faces would be a body of water with
380 ways out of it, which is the campaign's one open machine finding on Z3.

`shots.json` is the authority on every camera: kind, yaw, pitch, field of view,
and for each eye shot the cell the body stands in, the direction it faces and how
many open cells lie ahead of it.

**One anchor's camera could not stand in its own cell.** `anchor/stand-back-2` is
the recess that holds the corpse, so its own cell is occupied; the renderer says
so (`DW0727`) and stands the camera three cells back and three down rather than
taking a shot from inside a skull. Its shot is not in this set for that reason,
and the two other recess anchors are the same shape of standpoint.
