# Saltstair, variant A — design record

The design of record is `campaigns/hillside/DESIGN.md` (§2–§6), shared by both variants of the hillside comparison and changed by neither. This file says only what is particular to this variant.

**The cut: A — one box per building and per connector** (`campaigns/hillside/DESIGN.md` §5.1). Nineteen boxes: eleven way boxes (the square, five flights, four street segments, the quay) and eight houses, the square pinned at `min: [65, 96]` and every other box placed by its seam. Eighteen seams: five `stair` (opening 6 × 4, `stair_in` the flight), five `walk` contacts (each flight's foot onto the next segment) and eight `door` (street to house). The ground outside every box is the heightmap commons (`terrain/peninsula.png`, a byte copy of `campaigns/hillside/terrain/peninsula.png`). Each box is detailed by its own program under `programs/`.

**The walk**: spawn on the square, down the main street, the objective on the quay.

**The judging set**: the six cameras of `campaigns/hillside/DESIGN.md` §6, as the site plan's `views[]` and as `design/cameras.json`; the five numbers, measured in `GENERATION.md`.

**The reference image**: `design/reference/view1-from-the-sea.jpg` with its sidecar, a copy of the shared one (its sidecar canonically formatted by `delvec fmt`), recorded in `design.json`. The image is the authority on look; §4 of the shared design is the authority on size and position.
