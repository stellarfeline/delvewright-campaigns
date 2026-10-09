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
- The level exists to prove building and connecting several structures in boxes at different `y` heights. One site plan, one `open` site, eleven boxes: nine entered places (one ground place, the Hearth, Loom, Seed and Watch Houses, the Watch Crown, three rope bridges) and two scenery places (Watch Roots, Hearth Crown).
- Geometry is re-derived from reference view 4, which governs where the views disagree: the four trees stand at the corners of a square, with bridges on three of its sides.
- Each tree is split a different way. The Watch Tree is three stacked boxes: scenery roots, house, entered crown. The Hearth Tree is three: entered glade, house, scenery crown (its crown is wider than its house's eaves reach). The Seed Tree is one box with a `roof`-zone crown. The Loom Tree is one sky-open box on a topped trunk with no crown.
- The bridges declare a ceiling (lid left as air by their pieces), because each hosts a stair 4–6 high and a sky-open place has only its class-minimum headroom.
- The forest floor is the commons and no place. A body that reaches it walks back to the first ladder through the Root Glade.
- Every ladder hangs on bark or on a post, because a vanilla ladder needs a sturdy face behind it.
- In-game text is English. A `zh-cn` sidecar is not asked for yet.

## Capability findings

These are open engine gaps that this design needs. They are recorded here and are not worked around.

1. **Every horizontal seam above the ground stands on a fixed column of earth.** Spec-0098 §2 rule 0 says the following, and `Site::ground_height` in `crates/dsl/src/siteplan/claim.rs` at engine `0a534fe2d` implements it: where a seam crosses a ring column, that column's ground height is the seam's sill minus one, whatever the terrain under it. `Site::fixed_cells` then fixes every ring cell from the claim's bottom up to that height as the whole's ground, in the site's terrain blocks, and no piece may write there (`DW0990`, first shape). Every bridge landing in this camp is a horizontal seam with its sill 12–20 blocks above the forest floor. So each of the six bridge seams would stand on a one-cell-thick wall of dirt, the width of its opening, from the forest floor up to the deck. No document can remove it. The rule is right for a doorway on the ground and wrong for a seam over open air: a bridge landing, a balcony door, a gangway. Status: open, and blocks the bridge half of the level.
2. **No edge class means "climb", and the blockout has no stand-in for one (suspected, not yet reproduced).** Spec-0099 makes a ladder climbable in the nav model, and it names a climb edge class as a non-goal: the seam's `form` is where the ladder is said. The layout graph's classes are `walk | stair | drop | barred | vision`. A rope ladder through a floor (14 and 9 rungs here) must be declared as one of them. As read at engine `0a534fe2d`: `DW0829`'s sill check skips a seam through a floor; the stage-5 derivation lays treads only for a `stair`; and a `walk` with a rise gets nothing. If that reading holds, a `walk` seam with a ladder `form` leaves the upper place unreachable at stage 5, before any piece can lay the ladder. A `stair` seam builds green only by massing a 16-course stair the design does not have. The round that writes the site plan reproduces this on the first release carrying spec-0098 before choosing either. Status: to confirm.
3. **The forest floor is dressed by a world edit, not by a place.** Spec-0098 §10 names dressing an `open` site's terrain (undergrowth, fallen logs, roots beyond a ring) as stage 7's edit script and a follow-on. The buttress roots stay inside each tree's footprint. Ferns, logs and small trees on the commons go through `world-edits.json`. This is the falsifier §10 names, and is recorded only to confirm when the level is built.
4. **Scenery places depend on PR #1010.** The Watch Roots and the Hearth Crown are boxes that are never entered. The declaration that makes a place scenery-only (no reach, no seam, not on any route) arrives with PR #1010. Until it lands, the two scenery boxes are planned but cannot be stated in a site plan.

## Build round on engine 5cdbc753 (PR #1010, dsl 0.38.0)

Built with `delvec 1.10.0, dsl 0.38.0, mc 1.21.11`, compiled in release mode from the read-only engine tree at `5cdbc75372812a8899a544d567bd71e55d293c56` and invoked by path (cargo exit 0). The skill pages are read at that revision. The toolchain's `env.sh` was not used; Init I1b is not run against it, because the engine this level needs is not released.

State at the pause: steps 1 to 9 done; `validate`, `analyze` and `build` exit 0; all 12 places are detailed (blockout binding: 12 detailed, 0 massed by the derivation); the DW0311 binding walks 8 of 8 legs; DW0921 reports 0 cells a body cannot leave. Not done: the cameras (8b), the machine ladder (10), the visual review (12) and the hand-over (13).

Each place is a grammar program under `programs/`, written by `design/programs-src/places.py` (the design, in world coordinates, from each place's handout fetched at run time) through `design/programs-src/thlib.py` (states completed from the pinned registry; contract regions cut out by guillotine; the rest band-compressed). `design/programs-src/lights.py` lists the finale's 23 lantern lines, read both by the pieces (their marks) and by the quests (their `fill-region` boxes).

### What the engine bent in the design

1. **A way is at least one grid quantum wide (`DW0825`).** The design wanted 3-wide rope bridges, 22, 20 and 22 long; they are 4 wide and 20, 20 and 24 long, and the trunk spacings follow from those lengths (42, 42 and 44).
2. **A place one cell from another place's ring, with nothing connecting them, is refused (`DW0827`).** A bridge's claim runs down to the ground under its deck, and so does the Root Glade's. The design wanted the glade 24 × 24 under the 24 × 24 Hearth House; at that size its ring shared cells with both bridges' ground columns. It is 20 × 20.
3. **The spatial contract cannot state a climb between two levels of one place.** An interior edge is proved by walking (`contract-edge-proof`: "a walk connects both ways, and this one does not"), so the 19-rung ladder from the Watch Crown's landing to the lookout ring had no contract form, while a climb between places is a first-class `climb` seam. The design wanted the ring as a second level inside the Watch Crown. It is now a fourth box on the Watch Tree, `node/crown-lookout`, reached by the seam `edge/lookout-ladder`.
4. **`DW0833` (`distance-xz`, built world) gives a false reading where a box's centre column is solid.** `blockout::built_span` probes outward from `PlacedBox::centre()` at the top course; when that cell is solid (a trunk at the centre), `built_centre` falls back to the box's integer centre, while an unobstructed box measures a half-cell centre. The Hearth–Loom distance measured 42.5 against a plan value of exactly 42. At stage 5, the stand-in ladder pillar in the Watch House also shortens the probe (44.045). The three spacing identities were `eq 42/42/44`; they are now `ge 42` and `le 44` on each side, the range DESIGN.md §4.1 states. **This is a loosening**, made because of this defect.
5. **Scenery owes no light, but the build measures a scenery piece's declared space.** `contract-reachability` refuses a scenery piece whose space holds no standable cell ("examined ZERO objects"), and the build's per-place `DW0210` then holds that one cell to light 3. The gallery's sealed beacon carries a lamp in its own lid. The Watch Roots and the Hearth Crown follow it: each has a one-cell sealed hollow in its trunk, floored with shroomlight, which no one sees.
6. **A half-detailed campaign stops walking at a climb.** When the lower place of a `climb` is bound and the upper one is still a stand-in, nobody hangs the rung in the hole cell of the upper place's floor course: the derivation hangs ladders only when the lower place is a stand-in. Reproduced with the Root Glade detailed and the Hearth House not: `DW0986` on `edge/glade-ladder`, and `DW0837` for every place beyond it. It cleared once the Hearth House was detailed.
7. **A piece's overview camera ignores a place stacked over it.** `render_plan`'s interior eye is 1.5 outside the piece's corner and 3 over its top; the Root Glade's landed inside the Hearth House's corner post (`DW0724` at [23, 87, 23]). Answered in geometry, as the rule says: every platform corner is a single fence, which no body climbs.

### Design decisions made in this round

- The Root Glade is closed by a hedge three high (fallen logs and bushes), open above to the light. Under every aloft place the ground is that place's own claim, so a walkable forest floor would run between places outside their seams. The commons is unwalked. DESIGN.md §Safety still says a body that reaches the ground walks back to the ladder; no body can reach it.
- Every rail is two fences high. A finale lantern line is a station, and a station stands in play space, so the ring rows are part of each floor's space; Lantern Night swaps the rail's top course for lanterns.
- A place's plane with its bridge is closed above the 3-high mouth (`DW0836`), so the Loom House's and the Seed House's bridge mouths are framed gateways.
- The Watch Crown's floor course and the lookout's are leaves round their planks (`DW0836`: a stacked plane joined by a seam is wall except at its opening). The rope ladder runs in a flute of bark from the Watch House to the lookout, so a climber can step off only onto the landing or the ring (`DW0921`).
- The three vistas' eyes stand at y 115, on the lookout's rim: the DDA counts the one-fence rail as solid at a standing eye.
- Lantern Night's sky is `{"moon": "high"}` under the world's new moon. `concept/lantern-night` records it, drawn this round and **waiting on the owner** (design/README.md).
