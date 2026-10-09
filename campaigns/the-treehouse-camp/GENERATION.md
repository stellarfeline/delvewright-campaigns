# The Treehouse Camp — generation record

## Toolchain

- Designed against the engine release `delvec--v1.10.0` (`delvec 1.10.0, dsl 0.36.1, mc 1.21.11`). Init I1b exits 0 against that release's skill page and binary.
- The design targets two engine surfaces the release does not have: spec-0098 (a place owns its outside; `fill: open` over heightmap terrain; seam `form`; per-place handout; ADR-0032), read at engine `0a534fe2d` on its feature branch, and spec-0099 (a body climbs), merged at engine `df833210d`. No stage document is written yet, and nothing is compiled. The site plan is written against the first release that carries both.
- Placement: a site plan. The camp's exterior is the whole point: four giant trees and their houses, seen from the ground, from each other and from the top.
- The reference views were drawn with `tools/creator/refimg.py` on `gemini-native` (`gemini-3.1-flash-image`). Before the series, the provider's image input was checked two ways. First, a probe image of a red triangle and a magenta square on yellow was passed as `--style-ref` with a prompt that named neither shape nor colour, and it came back as the same picture. Second, the probe call's sidecar reports 1120 image input tokens.
- The engine constitution's operating half (`CLAUDE.local.md`) was in force for this run.

## What the brief pinned, and what was invented

Pinned: a clan's camp deep in a great forest, in the spirit of the great tree villages of a well-known film; several treehouses built around the waists of several giant trees; rope ladders and rope bridges between them; houses at different heights, on trees growing from ground at different heights; small and refined. A showcase of 15–30 minutes for 1–4 players, with no combat or very little.

Invented: everything named in `DESIGN.md`: the Greatwood, Lantern Night, the four trees and five houses, the cast, the quarrel, and the route. "In the spirit of" is taken as one idea only (people living high in giant trees, moving on rope). No franchise name, likeness or design is used (`DESIGN.md` §1).

## Posture note

This campaign pushes three axes off the machine default (skill *writing craft* §B). **Feelings are named outright**: Tobi says he is afraid of the ladder, and Oru says she is sad not to climb. **A subplot is left unresolved**: Neve and Hessel's quarrel over the Low Bridge is told from both sides and never settled. **The escalation is uneven**: a quiet errand ends in one beat larger than all the rest, when the whole camp lights up at once.

## Decisions

- No combat. The showcase is the place and the climb.
- One site plan, one `open` site, nine places: one ground place, five treehouses, three rope bridges.
- The forest floor is the commons and no place. A body that reaches it walks back to the first ladder through the Root Glade.
- Every ladder hangs on bark or on a post, because a vanilla ladder needs a sturdy face behind it.
- Each crown is its treehouse's declared `roof` zone. The Watch House has no `roof`, because the Crown Lookout is stacked over it, so the Watch Tree's lower crown sits inside the Watch House's headroom.
- In-game text is English. A `zh-cn` sidecar is not asked for yet.

## Capability findings

These are open engine gaps that this design needs. They are recorded here and are not worked around.

1. **Every horizontal seam above the ground stands on a fixed column of earth.** Spec-0098 §2 rule 0 says the following, and `Site::ground_height` in `crates/dsl/src/siteplan/claim.rs` at engine `0a534fe2d` implements it: where a seam crosses a ring column, that column's ground height is the seam's sill minus one, whatever the terrain under it. `Site::fixed_cells` then fixes every ring cell from the claim's bottom up to that height as the whole's ground, in the site's terrain blocks, and no piece may write there (`DW0990`, first shape). Every bridge landing in this camp is a horizontal seam with its sill 12–20 blocks above the forest floor. So each of the six bridge seams would stand on a one-cell-thick wall of dirt, the width of its opening, from the forest floor up to the deck. No document can remove it. The rule is right for a doorway on the ground and wrong for a seam over open air: a bridge landing, a balcony door, a gangway. Status: open, and blocks the bridge half of the level.
2. **No edge class means "climb", and the blockout has no stand-in for one (suspected, not yet reproduced).** Spec-0099 makes a ladder climbable in the nav model, and it names a climb edge class as a non-goal: the seam's `form` is where the ladder is said. The layout graph's classes are `walk | stair | drop | barred | vision`. A rope ladder through a floor (16 and 24 rungs here) must be declared as one of them. As read at engine `0a534fe2d`: `DW0829`'s sill check skips a seam through a floor; the stage-5 derivation lays treads only for a `stair`; and a `walk` with a rise gets nothing. If that reading holds, a `walk` seam with a ladder `form` leaves the upper place unreachable at stage 5, before any piece can lay the ladder. A `stair` seam builds green only by massing a 16-course stair the design does not have. The round that writes the site plan reproduces this on the first release carrying spec-0098 before choosing either. Status: to confirm.
3. **The forest floor is dressed by a world edit, not by a place.** Spec-0098 §10 names dressing an `open` site's terrain (undergrowth, fallen logs, roots beyond a ring) as stage 7's edit script and a follow-on. The buttress roots stay inside each tree's footprint. Ferns, logs and small trees on the commons go through `world-edits.json`. This is the falsifier §10 names, and is recorded only to confirm when the level is built.
