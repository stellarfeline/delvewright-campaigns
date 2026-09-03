# Approved design — the Saltworks at Greyhithe

Approved 2026-09-03 at the `/new-delve` design gate.

**Author from the image, judge against it, present every choice beside it.**

## The map's reference (`reference/`)

Four views of one subject, in one hand. View 1 was drawn from the prompt alone
and is the series anchor; views 2, 3 and 4 each carry its interaction id in
their sidecar's `request.chain_from`.

| view | file | what it is authority for |
|---|---|---|
| 1 | `map-v1-sea-elevation.jpg` | **the silhouette from the sea** — the whole site in one frame, and the anchor every other image in this campaign is drawn against |
| 2 | `map-v2-plan.jpg` | the arrangement of the parts, in plan |
| 3 | `map-v3-works.jpg` | the works terrace, close enough to read the masonry |
| 4 | `map-v4-precinct.jpg` | the precinct and the headland |

**Reference imagery is style authority and never dimensional authority.** Every
number this campaign is built to lives in `geometry-brief.json`, and where a
view disagrees with a fact the fact wins. Two known disagreements in view 2,
approved as they are: it carries the words "NORTH SEA" against the style note's
"no text", and its proportions read square where `fact/site-span-east-west` and
`fact/site-span-north-south` say 320 by 128.

## The scenes (`concept/`)

Twenty-four places, a near view and a far view each, named `<place>-near.jpg`
and `<place>-far.jpg`. Near is the scene as a player stands in it; far is the
same scene in its surroundings.

Every one of the forty-six was drawn against view 1 under the campaign's one
style note, which is why the boiling house, the chapter house, the works yard
and the light court read as one builder: one masonry, one repeated
round-headed opening at four scales, one dusk, one warm lamp.

**Two views are approved absent** and are not owed:

| place | view | why |
|---|---|---|
| `drowned-pans` | far | the call timed out and the round was at its image budget |
| `cloister-walk` | near | the call timed out and the round was at its image budget |

Their near / far partners carry the design for those two places.

## What the images are authority for

1. **One masonry.** Grey limestone in long thin courses, iron-stained where the
   sea reaches it, dressed square at every jamb and quoin.
2. **One way of letting light in.** Tall narrow round-headed openings, high in
   the wall, in a repeated rhythm, at four scales.
3. **One silhouette from the sea.** Low at the water, rising in two steps,
   ending in the light — judged from `view/from-the-sea` in the site plan.

The sidecar beside each image carries its prompt, style note, resolved frame
and anchor id, so any view can be re-issued with one word changed.
