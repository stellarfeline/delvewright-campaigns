# Z2 门楼 — review set

Judged against `../../concept/z2-gatehouse.jpg` for the interior, and against
`../../reference/map-v1-front-elevation.jpg` and `../../reference/map-zones.md`
for what the shore sees and where the zone sits.

**Built at the seed the manifest declares.** `programs/zones.json` builds this
zone at **25 × 18 × 56, seed 1**, and every image here is that expansion.

## Which anchor answers which question

| image | where the body stands, facing | the question it answers |
|---|---|---|
| `eye-look-gate-in.png` | the passage at 10,4,47, south | **2.1** — the portcullis is DOWN, and the shore is on the far side of it. This is the first thing the cliff road puts the player in front of |
| `eye-look-passage.png` | the winch bay at 10,4,23, south | **2.6** — the winch's own view: the whole passage, the vault stepping over it, and the shut gate at the end of it. This is the frame `TIDE-1` fires into |
| `eye-look-embrasure.png` | the passage at 10,4,31, west | **2.4** — the grate across the porter's embrasure, its sill, and behind the bars the lodge floor with the leaves on it and the bound ledger on its stand |
| `eye-look-lamp.png` | the passage at 10,4,39, west | **2.7** — the niche the lampman takes, and the one block in this zone that emits light |
| `eye-look-drain.png` | the passage at 14,4,49, south | **2.3** — the gutter and its two mitred kerbs running the length of the flags and out under the gate. It is dry, and that is a decision, not an omission (below) |
| `eye-look-yard.png` | the yard at 12,4,10, south | the gatehouse's inner arch from the ground S3's banded door drops on to, with the winch framed in it |
| `eye-murder-watch.png` | the chamber at 11,11,36, north | **2.2**, the half the passage cannot show: there IS a storey over the vault, it is walked, and the murder-holes are openings in **its** floor |
| `eye-gatewright.png` | the leads at 12,16,33, north | **2.5** — the roof above the murder-holes, the winch that has nothing left to lift, and the ground the elite is fought on |
| `eye-stair-head.png` | the stair at 19,11,36, north | the climb: the mid landing, level with the chamber's floor, and its doorway west |
| `eye-gateway.png` | the gate arch at 10,4,55, north | the gate front from outside, once the portcullis is up: what a body walks into off the flat |
| `ext-se.png`, `ext-sw.png` | — | massing from the shore side: a squat pale block on a rock footing, its roof flat, walkable and crenellated, with the yard stepping down behind it |
| `ext-nw.png` | — | the same from behind: the yard, its curtain, and the lip the causeway head drops over |
| `top.png` | — | the plan: the passage's centre line, the four murder-holes on it, the lodge and the stair well either side |

## Reproducing the set

```sh
delve-grammar expand --file design/programs/z2-gate-ward.json \
    --region 25x18x56 --seed 1 --traversable --allow-falls \
    --id z2-gate-ward -o out/
delve-render --size 900 piece out/z2-gate-ward.json -o shots/
```

The zone is past the 48-per-axis cap, so `out/` holds two tiles and one
manifest; `delve-render piece` is given the **manifest** and assembles them
into one scene.

Six of the standpoints are **review standpoints, not campaign anchors.** The
program declares none of them and the anchor set a campaign binds to is
unchanged; they are added to the expansion's metadata before rendering. The
renderer has no author-aimed camera — the aiming instrument is a declared
anchor with a position and a cardinal facing, which is why a standpoint is a
piece of data rather than a command-line flag:

| name | pos | facing |
|---|---|---|
| `anchor/look-gate-in` | 10, 4, 47 | south |
| `anchor/look-passage` | 10, 4, 23 | south |
| `anchor/look-embrasure` | 10, 4, 31 | west |
| `anchor/look-lamp` | 10, 4, 39 | west |
| `anchor/look-drain` | 14, 4, 49 | south |
| `anchor/look-yard` | 12, 4, 10 | south |

## What these renders cannot show

- **The camera is level and cannot look up.** So no image here shows the
  murder-holes from underneath, or the man on the roof from the yard — the two
  places the beat sheet asks a player to look *up*. `eye-murder-watch.png`
  shows the same openings from above instead, and `eye-gatewright.png` shows
  the roof from on it. Judge the openings' position and count from `top.png`
  and the chamber shot; the upward view is a thing the assembled world has and
  this instrument does not.
- **Both end faces open on to other zones.** The west face is the breach the
  cliff road ends at and the north face is the causeway head; beyond each the
  renderer has nothing to draw. `eye-causeway-head` is therefore an empty frame
  and is deliberately not in this set — what that anchor is about lives in the
  assembled world.
- **Light is placed, not measured.** One lantern is placed; the metadata says
  `"profile": "unmeasured"` and means it. The number comes from
  `delve-admit lighting`, on the assembled world.

## Two things in these images that are deliberate departures

- **The channel is dry.** The concept paints a running stream down the middle
  of the flags. `tide.md` forbids both a bounded basin and flowing water: the
  sea is one whole-world plane, so this zone paints no water at all and builds
  the gutter one course below the flags with its invert at the height the tide
  document gives it. At the ebbs it is a dry gutter and at the flood the plane
  fills it, which is the whole of that document's Z2 row. The zone contains
  zero water blocks, and that is checked rather than asserted.
- **The ironwork is grey, and the concept's is rust.** The concept's grate
  reads `#62544b` at its lit 90th percentile — a warm brown. `iron_bars`
  measures `#898b88`, a neutral grey. The block that carries the hue is
  `exposed_copper_bars` (`#866c59`), and the admission allowlist does not carry
  the copper bar family; widening it to admit one asset is the bypass its own
  diagnostic names. So the gate ships grey.
