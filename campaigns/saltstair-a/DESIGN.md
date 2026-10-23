# Saltstair, variant A — design record

**The design of record is `campaigns/hillside/DESIGN.md`, unchanged.** This campaign is its variant A (§5.1): one site-plan box per building and per connector. That file's §2–§6 are the authority on everything — the peninsula, the town, the geometric facts, the cut, the judging set — and the heightmap (`terrain/peninsula.png`, a byte copy of `campaigns/hillside/terrain/peninsula.png`) and the reference image (`campaigns/hillside/design/reference/view1-from-the-sea.jpg`) are the ones it names. Nothing in this campaign departs from it; a departure would be a change to that file first.

What that file leaves to this campaign, and this campaign states:

- **Id and directory**: `saltstair-a`, `campaigns/saltstair-a/` (that file names the variant's directory `campaigns/hillside-a`; the id is this campaign's own).
- **A demo level**: `world.json` declares `demo_level: true`.
- **The plan**: nineteen boxes, the nineteen rows of §4.1 and §4.2; the square pinned at `[65, 96]`; the eighteen seams of §5.1's table, five `stair`, five `walk` contacts, eight `door` walks. The ground outside every box is the heightmap.
- **The story**: one quest, one objective — reach the quay; no cast.
- **Nineteen pieces**, one program each, written at step 9 in critical-path order (the eleven street places from the square to the quay), then the eight houses.

## Beats

| Beat | Place | What happens |
|---|---|---|
| arrival | `node/square` | the party spawns on the square at the top of the town |
| the walk | the main street | five terraces and five flights down |
| the goal | `node/quay` | reaching the quay completes the delve |
