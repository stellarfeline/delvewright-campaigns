# The Treehouse Camp — generation record

## Toolchain

- Built on spec-0098 (a place owns its outside; boxes as cuboids; `fill: open` over heightmap terrain; seam `form`; the per-place handout; the contract `climb` edge; ADR-0032) and spec-0099 (a body climbs), at the engine revision the last section names. No release carries them yet.
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
- The bridges are sky-open (`ceiling: {open: n}`), with headroom enough for the plank steps each hosts (4–6 high), and hang one course of beams under their decks (`base: {aloft: 1}`).
- The forest floor is the commons and no place. A body that reaches it walks back to the first ladder through the Root Glade.
- Every ladder hangs on bark or on a post, because a vanilla ladder needs a sturdy face behind it.
- The delve ships in English and Chinese (`l10n/zh-cn.json`), transcreated on DeepSeek by `tools/creator/i18n-translate.py` and held to one rendering per place name by hand.

## Capability findings

The four engine gaps this design was written against, and where each stands:

1. **A seam aloft stood on a column of earth.** Corrected in spec-0098 (correction 1: a seam aloft fixes no earth), and boxes now hang (`base: aloft`). Closed.
2. **No edge class meant "climb".** The layout graph has `climb` (correction 2), and a piece's contract has a `climb` edge for a ladder between two of its own levels (departure 33). Both are used here. Closed.
3. **The forest floor is dressed by a world edit, not by a place.** Confirmed: the lantern posts on the commons are set by `world-edits.json`. Ferns, logs and small trees on the commons would go the same way; none are added yet.
4. **Scenery places.** `reached: false` is declared on the Watch Roots and the Hearth Crown, and the battery proves both not reached. Closed, with the light pair in the round record below.

## Build round on engine 442c3e7c (dsl 0.38.0, grammar program 1.10.0)

Built with `delvec 1.11.0, dsl 0.38.0, mc 1.21.11`, force-rebuilt in release mode from the read-only engine tree at `442c3e7ca2ce52e52ac208d4cd361d82037dea65` (cargo exit 0) and invoked by path. The skill pages are read at that revision. The toolchain's `env.sh` is not used: the engine this level needs is not released.

Each place is a grammar program under `programs/`, written by `design/programs-src/places.py` (the design, in world coordinates, from each place's handout fetched at run time) through `design/programs-src/thlib.py` (states completed from the pinned registry; contract regions cut out by guillotine; the rest band-compressed). `design/programs-src/lights.py` lists the finale's 23 lantern lines, read both by the pieces (their marks) and by the quests (their `fill-region` boxes). `terrain/heightmap.py` writes the forest floor; `terrain/lanterns.py` writes `world-edits.json`, the lantern posts on it.

### State

- `validate`, `analyze` and `build` exit 0; `detail --all` exits 0. Blockout: 11 places detailed, 0 stand-ins. Battery: 11 places reached, 2 of them scenery, proven not reached. All 15 identities hold, the four trunk spacings exactly (44, 42, 42, 44).
- DW0311: 8 of 8 legs walked. DW0921: 39,760 cells a body can reach, 0 it cannot leave.
- PackTest: 41 of 41 required tests pass.
- Bot critical path: **red**, blocked by the toolchain defect in the next list.
- Staging gate: stageable, no override.

### What the engine still bends, and what it no longer does

Undone on this engine:

- **Way width (`DW0825`).** The bridges are 3 wide and 22, 20 and 22 long, at the designed trunk spacing.
- **The lookout as its own box.** The Crown Lookout is a second level inside the Watch Crown, joined to the landing by a `climb` edge of the crown's contract.
- **The spacing identities.** They are exact again (`eq`). DW0833 reads each floor's centre.
- **Size and way classes.** None is declared.
- **The forest floor.** The bridges, the Hearth House and the Watch House and crown hang (`base: aloft`). The forest floor under and between them is the commons, walkable everywhere: the terrain is a harmonic field between the four ground pads and the rim, with no step over one block and no pit. The Root Glade opens onto it, so a body that reaches the ground walks back to the first ladder.
- **The sealed lit hollows.** The scenery pieces no longer carry them.

Still bent (recorded here, not worked around):

1. **The Root Glade is 20 × 20, not 24 × 24 (`DW0827`).** The glade's open headroom must reach y 84, one course under the Hearth House floor, for the climb into it. At 24 × 24 its ring column (x 48 and z 48) shares cells at y 78–84 with the Long and Low Bridges' undersides, and no seam joins the glade and a bridge to award them. Reproduced on this engine: "the cuboids of `node/long-bridge` and `node/root-glade` all claim 30 cell(s) and no rule awards them" (and 20 for the Low Bridge).
2. **A scenery piece with standable surfaces owes light.** Departure 32 lets a scenery piece state zero standable cells only when none of its cells is standable. A crown's leaf tops are standable, so its contract must declare one standable cell in a space (`contract-reachability` refuses a space with none), and the build's DW0210 then holds that cell to light 3. The Hearth Crown answers with the hall's festival lanterns, hung from its great arms over the platform, beside the declared cell on the east arm.
3. **Toolchain defect: a climb is exported across two ladder columns.** Leg 6 of `validation/critical-path-waypoints.json` carries one climb with `bottom` [74, 84, 78] and `top` [74, 111, 79]. The body climbs the Watch House ladder (column z 78) into the landing's hole, steps over the top onto [74, 93, 79], which is both standable and the foot of the crown's own ladder (column z 79), and climbs that to the ring. The exporter does not end the climb at the standable cell, so the two columns are merged, and the harness refuses the record: `waypoints/legs/6/climbs/0 bottom and top must be one column, bottom not above top` (bot exit 1). The ladders are not moved to dodge it.

### Design decisions made in this round

- Every rail is two fences high. A finale lantern line is a station, and a station stands in play space, so the ring rows are part of each floor's space; Lantern Night swaps the rail's top course for lanterns. A platform corner is a single fence.
- A place's plane with its bridge is closed above the 3-high mouth (`DW0836`), so the Loom House's and the Seed House's bridge mouths are framed gateways.
- The Watch Crown's floor course is leaves round the landing's planks (`DW0836`). The Watch House's ladder tops out in the landing's hole; the crown's own ladder starts on the landing beside it and climbs a flute in the bark (ribs either side, clear air west of it) to the ring, so a climber can step off only onto the landing or the ring (`DW0921`).
- The forest floor is lit by design: 29 lantern posts under the three bridges and round the trees' feet, set by the edit script. The plan declares no `lighting`, so the relight pass sets no torch.
- The three vistas' eyes stand at y 115 on the lookout's rim: the DDA counts the one-fence rail as solid at a standing eye.
- Lantern Night's sky is `{"moon": "high"}` under the world's new moon. `concept/lantern-night` records it: drawn earlier, and **waiting on the owner** (design/README.md).
