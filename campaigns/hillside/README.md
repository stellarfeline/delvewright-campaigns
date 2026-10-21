# Saltstair — the shared design of the hillside comparison

Not a campaign: this directory carries no `world.json`. It holds what the two variants of the hillside-town comparison share, so that neither can drift from the other:

- `DESIGN.md` — the design brief (the town, the peninsula, the two cuts, the judging set);
- `terrain/peninsula.py` → `terrain/peninsula.png` — the one heightmap both variants declare as their `fill.terrain.heightmap`, over `terrain/heightfield.py`;
- `design/reference/` — the one reference image, its sidecar, its prompt and the style contract; each variant copies the image and sidecar into its own `design/reference/` and records it in its `design.json`;
- `design/thlib.py` — the voxel-to-program compiler the feasibility fixture's piece is written with, a copy of `campaigns/the-treehouse-camp/design/programs-src/thlib.py`.

The variants are `campaigns/hillside-a` and `campaigns/hillside-b`; the feasibility fixtures are `campaigns/hillside-feas-a` and `campaigns/hillside-feas-b`.
