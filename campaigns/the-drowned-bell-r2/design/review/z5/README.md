# Z5 hall keep — review set

Which camera answers which question. The authority on what each camera did is
`shots.json`, written by the renderer on every run: it names every shot with its
kind, yaw, pitch and field of view, and for each eye shot the cell the body
stands in, how that cell was chosen, and how far the view runs before something
stops it.

**The cameras are fixed.** Yaw, pitch and field of view are properties of the
shot kind; no flag aims one. The only camera a program can place is the eye
camera, which stands at a declared anchor and looks the way that anchor faces —
so **an anchor is the aiming instrument**, and the set below is the set this
zone's fourteen anchors make possible. Where a question below has no camera, it
is because no anchor stands where it would have to stand.

**Read the eye shots first.** This zone is an interior. Its exterior orbit
cameras photograph a closed mass, for the same reason a cliff section's do: there
is no elevation to see, and nothing outside the piece answers a question about
the hall.

| Shot | The question it answers |
|---|---|
| `eye-hall-door.png` | Does the hall read as an intact great hall? Stands in the hall doorway looking down the length: the timber-beamed ceiling, the ashlar side walls and the flagged floor in one frame. This is the zone's identity shot. |
| `eye-bait.png` | What does a body see from the hall floor — the wall surface, the hanging strands, and a roof post at arm's length. Judge the masonry's variation here; at distance zero it is the wall. |
| `eye-bait-perch.png` | The gallery perch above the hall, looking down its length. Answers whether the hall reads as one volume from above and whether the beam grid is legible. |
| `eye-store-line.png` | Does the store lane read as a keep's stores? The barrel line runs away down the floor with the ashlar wall beside it. |
| `eye-alcove.png` | The alcove and its pedestal at close range — the one place fine surface is seen from within arm's reach. |
| `eye-landing.png` | **Evidence for an open item.** The lower landing the descent ends on. It is bare floor: the frame contains no built content at all. |
| `eye-hatch.png` | **Evidence for an open item.** This anchor stands inside the inert margin mass, so its eye camera looks into solid rock rather than at a scene. |
| `top.png` | The plan: the zone's length, where the hall sits against the stores and the lower keep, and the tile-set assembled as one scene. |
| `ext-se.png`, `ext-nw.png` | Massing only, and they are the weakest shots in the set — a roofed interior photographs as a closed box from outside. They are here to show the envelope, not the building. |

The zone is 76 long, past the 48-per-axis structure-template cap, so it ships as
two tiles and a manifest. Every camera above framed the **assembled** zone: the
renderer reassembles the tiles before it places a camera, so no shot is cut at a
packaging plane and a body looks straight across the seam. The seam falls at
z=48, inside the hall, and no shot in this set shows a discontinuity there.
