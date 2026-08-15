# Z3 下沉外庭 — Drowned Ward · review set

Which camera answers which question. `shots.json` is the authority on what each
one did — its kind, yaw, pitch, field of view, and for every eye shot the cell
the body stands in and how far ahead the view runs.

The zone is 40x10x60 and ships as two tiles; the renderer reassembles them, so
every camera here frames the whole ward and a body can look straight across the
packaging cut.

## Read the eye shots first

The cameras are fixed. There is no author-aimed camera in this toolchain: the
aiming instrument is the program's own declared anchors, and an anchor gets an
eye shot only if it carries a **position and a cardinal facing**. Every anchor
below is declared with both.

| Shot | The question it answers | Beat |
|---|---|---|
| `eye-causeway_head.png` | Does the ward read from the gate — a raised spine above the water, arcades standing in it, the tower at the far end, the whole route visible without turning? | 3.1 |
| `eye-wader_4.png` | What the ward looks like from *in* the water: open sea, the ruined arcade between you and the spine. Where the answered stand. | 3.2 |
| `eye-weed_pinch_1.png` | The first weed heap against the kerb, and how far it narrows the lane. | 3.3 |
| `eye-weed_pinch_2.png` | The second, against the other kerb — one rule handed its own reflection. | 3.3 |
| `eye-wreck_2.png` | A sunken boat at the waterline, off the spine's left, with the tower and its barred door beyond. Shows what leaving the causeway costs. | 3.4 |
| `eye-arcade_climb.png` | From the head of the fallen bay, looking back down the climb: how a body gets from the causeway up to the arcade deck. | 3.6 |
| `eye-arcade_walk.png` | The intact arcade deck as the upper route, running level into the tower's flank. | 3.6 |
| `eye-shutter.png` | The shutter-height opening the arcade walks in through. | 3.6 |
| `eye-tower_upper.png` | The gate gallery, looking through the cross-wall door into the chamber beyond. | 3.6 |
| `eye-descent.png` | The head of the descent — the well in the mid-storey floor and its treads. | 3.6 |
| `eye-tower_hall.png` | The undercroft: ranked piers carrying the oversail, and the lane between them to the way on. | 3.6 |
| `eye-barred_door.png` | Shortcut **S2** from the inside — the door that does not open from the causeway side. | 3.7 |
| `eye-grate_landing.png` | Where the cistern grate (**S4**) comes out onto the ward floor. | 3.8 |
| `eye-tower_gate.png` | **An empty frame, and it should be.** The way on faces out of the zone's exit face, so what it is about lives in the assembled world, not in a per-piece render. Kept in the set so the gap is visible rather than quietly dropped. | — |

Twelve `anchor/wader-*` are declared and only one is shown; the other eleven are
the same shot at eleven other stations along the two flats.

## What the exterior cameras can and cannot show

`ext-nw.png`, `ext-se.png` are corner three-quarters and `top.png` is the plan.
They show the massing — two arcades, the spine between them, the tower at the
head — and the plan is the clearest picture of the layout in the set. They
**cannot** show the tower square-on: every exterior camera sits on a corner
bearing and none tilts up, so there is no elevation of any face here. The
tower's near face is read from `eye-causeway_head.png` and `eye-weed_pinch_1.png`
instead, which is where a player sees it from anyway.

The ward is open to the sky, so the plan is a real plan rather than a picture of
a roof — the one thing it hides is the tower's two storeys, which are under the
one roofed part of the zone.
