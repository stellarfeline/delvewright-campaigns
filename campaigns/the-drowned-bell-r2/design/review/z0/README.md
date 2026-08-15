# Z0 barrow shore — review set

Eleven images and the shot manifest, from one render of the zone's own tile set.
**The renderer has no author-aimed camera**: yaw, pitch and field of view belong
to the shot kind, and the only thing that aims anything is the program's own
declared anchors. So the question each image answers is decided by where an
anchor sits and which way it faces, and an anchor that faces the wrong way
produces a picture of the wrong thing. Every anchor below was placed for the
beat it stages, not for the camera; where the two disagreed the anchor moved and
the geometry moved with it.

Reproduce the whole set:

```sh
# engine at the commit `zone-audit.yml` carries in GRAMMAR_REF
cargo build -p delvewright-grammar --bin delve-grammar --release
delve-grammar expand --file design/programs/z0-barrow-shore.json \
    --region 40x18x80 --seed 1 --traversable --id z0-barrow-shore -o out/

# the render crate is its own cargo workspace
cargo run --release --manifest-path crates/render/Cargo.toml --bin delve-render -- \
    --textures <1.21.11 client jar> --size 900 piece out/z0-barrow-shore.json -o shots/
```

`out/z0-barrow-shore.json` is the tile manifest, and it is what both commands
take. Handed a single tile instead, `delve-render` renders a fragment of the
zone and `delve-admit audit` refuses outright and names the manifest.

## Which image answers which question

| image | anchor / camera | the question it answers |
|---|---|---|
| `eye-wake.png` | `anchor/wake`, facing north | **The establishing shot.** Is this the concept image? Do the three tide-stakes read as one line from where the player wakes? Is the citadel's sightline clear? |
| `eye-grave_2.png` | `anchor/grave-2`, facing north | Do the cairns read as graves rather than as rubble, and do they visibly thin going inland? |
| `eye-first_answered.png` | `anchor/first-answered`, facing north | Is there open ground beside a cairn for a body to push up out of and walk landward past the player? |
| `eye-stake_2.png` | `anchor/stake-2`, facing north | Does a stake read as a rusted iron stake at one block, and does the ground change colour at the line? |
| `eye-lampman.png` | `anchor/lampman`, facing south | Is there a shelf, is the lamp lit on it, and does a man standing there see the whole flat? |
| `eye-ledge_foot.png` | `anchor/ledge-foot`, facing north | Does the flat end at a wall of rock with exactly one cut ledge starting up it? |
| `eye-mire_1.png` | `anchor/mire-1`, facing north | From the ground below the stake line, does the step up to the flat read, and is the mire visibly a different, softer ground? |
| `eye-crossing.png` | `anchor/crossing`, facing south | **Deliberately an empty frame**, and it is in the set for that. This anchor faces out of the piece into the fog band, so what it is about does not exist inside these bytes; its real view is the assembled world's own player-POV shot. The renderer says so as `DW0727`. |
| `ext-nw.png`, `ext-se.png` | orbit, fitted from outside | The massing: the flat's length against the crag's height, the crag's battered face, and the cut through it. |
| `top.png` | straight down, top layer stripped | The plan, and the one thing no eye shot shows: the cairn density gradient, sparse under the crag and crowding to the tide-line. |

`shots.json` records, per shot, the kind, yaw, pitch, field of view and eye
height, and for every eye shot the anchor's declared cell, the cell the camera
actually stood on, its offset, and how many open cells lie ahead before the view
is stopped. **A camera that stepped back is invisible in its own frame**, so six
of them are written down there rather than implied: the three graves and the
three stakes all put a solid block on their own anchor cell — the call
`store_room` makes for its barrel — so the camera stands one to three cells back
along the facing and the thing the anchor names stays in shot.

## What no image in this set shows

- **The sea.** The zone paints no water. The tide is one whole-world plane
  (`../../tide.md`) and a zone that painted its own would be the bounded basin
  that document forbids, so what these images show is the ground: the flat dry,
  and the ground below the stake line bare. That is the state at the Dead Ebb.
  At `T-EBB1`, where the delve opens, the plane stands one course higher and the
  mire is under it.
- **Anything standing on the anchors.** Thirty-seven anchors are declared and
  nothing occupies them; the lampman, the first of the answered and the figures
  in the silt are campaign content bound at generation time.
- **The citadel.** Z0 is the standpoint the whole silhouette is composed for, and
  everything it is composed of is another zone. What these images can show is
  that Z0 leaves the view clear, which is measured rather than looked at: the
  tallest thing this zone builds on the sight corridor subtends 11.2° from the
  wake point against the 27° the crown needs, and a three-course heap would have
  to be nearer than 2.7 blocks to stand in front of it.
