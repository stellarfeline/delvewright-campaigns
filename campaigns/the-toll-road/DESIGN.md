# The Toll Road — design record

The demo level for traps: a short fortified pass where every trap type guards
one alcove of loot, and disarm levers teach counterplay.

## Layout

One walled pass, `node/pass`, fifteen blocks across and thirty-seven long,
open to the sky. The road runs five wide down the middle from the foot of the
pass (south, where the party arrives) to the toll bar (north). Five blocks of
wall stand on each side, and the four strongrooms are cut into them. Past the
toll bar is `node/far-road`, a short stretch of road running on out of the gap.

The strongrooms, from the foot of the pass to the head:

| strongroom | side | trap | how it is sprung | what it does | counterplay |
|---|---|---|---|---|---|
| the toll booth | east | a `step` trigger on a stone plate in its mouth | stepping on the plate | rings a bell in the wall, and the actionbar says the wardens heard every step | none needed: it is harmless, and it is the lesson |
| the stair | west | `trap/stair-volley`, a pressure plate on the landing | stepping on the plate at the top of the stair | three salvos of arrows from a slot over the landing, blanketing the landing and the stair | the lever beside the mouth, on the road side; or the shield from the booth |
| the dart gallery | east | `trap/dart-gallery`, a tripwire across the gallery | walking through the string half-way along | three salvos of arrows down the gallery from a slot in its far wall | the lever beside the mouth; or cutting the string with shears (not in the kit) |
| the strongbox | west | `trap/strongbox`, the trapped chest itself | opening the chest | the loose roof in front of the chest comes down as gravel, once | the lever beside the mouth |

Every lever stands on the road wall beside its strongroom's mouth, where a
body standing on the road can reach it without stepping into the trap. The
toll bar's winch lever stands on the wall beside the bar.

## Beats

1. The party arrives at the foot of the pass.
2. The toll booth: the bell plate rings, and nothing else happens. The barrel
   behind it holds a shield and the toll schedule.
3. The stair, the dart gallery and the strongbox: optional; each barrel or the
   strongbox holds the old toll takings.
4. The winch lever at the head of the pass raises the toll bar
   (`obj/raise-the-bar`; `flag/bar-raised`, `open-gate anchor/seam-toll-bar`).
5. The party walks through onto the far road (`obj/through-the-gap`), and the
   campaign completes.

No branch, no ending table, no cast.
