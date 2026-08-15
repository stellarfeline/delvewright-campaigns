# Z6 cistern deep — the review set

`z6-cistern-deep`, expanded at 40x10x100, seed 1. Thirteen level shots from
inside the vault, one exterior pair and the plan. `shots.json` is the authority
on what every camera did — yaw, pitch, field of view, the cell each body stands
in, and how far ahead the view reaches before something stops it.

**Read the eye shots first.** The zone is a roofed vault, so the exterior orbit
cameras photograph the crown: `ext-nw` and `ext-se` are two pictures of the same
slab and cannot show that there is a room inside it. They are here to confirm
the outside is a closed mass with one break in it, and for nothing else.

## Which camera answers which question

| shot | stands at | looks | the question it answers |
|---|---|---|---|
| `eye-duct` | `11,7,96` | north | Is the way in a duct a body walks stooped, and does the vault open under it? Fourteen cells ahead before the floor stops the view — the drop is past that. |
| `eye-landing` | `12,4,87` | north | Does the vault read as the largest interior in the delve from the cell a body lands in? Thirty-two cells of clear nave. |
| `eye-vault_watch` | `12,4,68` | north | Is the plan legible — do the transverse arches rank away, and does the arcade read as a second line of them? |
| `eye-channel_watch` | `12,4,44` | south | The supply channel, the debris and the break in one frame, looked back across. |
| `eye-channel` | `12,4,50` | north | The near lip of the channel: what a body sees walking on to it. |
| `eye-shaft` | `13,7,52` | north | Standing on the debris under the break. The crest is paving, not rubble, so a body stands on it; the grey above is open sky through the collapse. |
| `eye-choir_watch` | `12,4,31` | east | Can the side vault be seen into from the nave without entering it? Twenty-six cells across the arcade, stopped by the breach's own grate. |
| `eye-choir` | `28,4,31` | west | What the side vault sees back: the arcade it is approached through. |
| `eye-breach` | `34,4,31` | east | Does the shortcut read as a hole smashed through the wall — barred, with a fallen sill and a pale broken lip? |
| `eye-grille` | `38,5,31` | east | The bars at arm's length, from the cell a campaign binds the shortcut to. Zero clearance: this camera is against its own subject and is not a picture of the breach — `eye-breach` is. |
| `eye-founder` | `12,4,17` | north | The arena: is the wellhead legible from where the fight happens, at the end of a vault that ends? |
| `eye-well` | `12,4,12` | north | The wellhead close: a dressed apron ring around a sunk mouth. |
| `eye-tongue` | `13,2,9` | south | From the bed of the well, on the silt: is there a way back out? Two one-block steps. |
| `top` | overhead | down | The crown, and the break in it. |
| `ext-nw`, `ext-se` | corners | down | The outside is a mass. See the note above. |

## What no camera in this set can show

- **The break, from below.** Every camera here is either level or pointing down;
  none tilts up. A hole in a crown is therefore unphotographable from the floor,
  and `eye-shaft` reaches it only because that body stands three courses up on
  the debris and the opening falls inside a level frame. `top` is the shot that
  shows the hole as a hole.
- **The channel's depth.** A level eye is 1.62 up and the frame falls away at
  roughly 0.7 of the distance, so no floor nearer than about two and a half
  cells is in shot. A body standing on the channel's lip cannot photograph the
  channel. `eye-channel_watch` frames it from beyond; the cut is three courses
  deep, and the expansion report's reachability pockets are what state that.
- **Water.** The cistern is wet in play and dry here on purpose: there is one
  sea and the campaign moves it (`design/tide.md`). Nothing in this piece
  authors a water block, so every shot is the room at a level below any tide.
- **Light.** The expansion places blocks, not photons. The renderer lights every
  surface the same, so the shaft of daylight the scene is built around is a hole
  in these pictures and not a beam.
- **The far ends.** A per-piece render has no neighbours, so a view that leaves
  the template shows flat background. The nave's own deep end is walled and the
  aisle's is not — that is the piece, not the camera.

## Anchors with no shot in this set

`anchor/break` (`12,4,55`, north) is declared and is where a body coming down
the nave first meets the debris. Its camera stands against the ridge's face with
zero clearance and photographs it, which says nothing a reviewer can use, so the
image is not kept here. The anchor is.
