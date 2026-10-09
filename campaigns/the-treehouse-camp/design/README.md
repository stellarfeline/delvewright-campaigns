# The Treehouse Camp — reference sheet

**Status: drawn, waiting for the owner's style confirmation.** Nothing here is approved yet. `design.json` is written at step 4, after the design gate.

These images are the authority on look and mood, never on position or size. The geometric facts are `../DESIGN.md` §4. Where an image and §4 disagree, §4 wins. Each view's drift from §4 is listed below so that nobody builds it.

## Map views (`reference/`)

All four views share one style contract (`reference/style.txt`, sent as `--style-note`) and are drawn at late afternoon, clear. Provider: `gemini-native`, model `gemini-3.1-flash-image`, `image_size` 2K. View 1 was drawn from its prompt alone. Views 2–4 were each chained on view 1's interaction (`request.chain_from` in each sidecar equals view 1's `id`), never on each other. Each chained call's sidecar records 1100 image input tokens, which shows that view 1's picture reached the model.

| View | Frame | Prompt | What it shows | Drift from §4 |
|---|---|---|---|---|
| `reference/view1-glade` | 16:9 | `prompt-v1-glade.txt` | From the Root Glade among the Hearth Tree's roots, looking up: the Hearth House, its rope ladder, the Long Bridge to the Loom House, and the Watch Tree's lookout far right. The series' style anchor. | The Loom Tree is drawn slim, not as a giant. The Long Bridge sags instead of climbing 4. |
| `reference/view2-plan` | 1:1 | `prompt-v2-plan.txt` | Straight down, north up, crowns lifted off: four square platforms, three straight bridges (Hearth–Loom east, Hearth–Seed south, Loom–Watch south), no Seed–Watch bridge, and the lookout ring over the Watch House. | Proportions are not to scale. The Hearth trunk is drawn off-centre on its platform, as a cut stump. |
| `reference/view3-south` | 21:9 | `prompt-v3-south.txt` | From the south, west to the left: platforms at different heights, the Watch Tree's long ladder up to the lookout above the crowns, the bridges between. | Bridges sag. The ground differences are softer than §4.2's 12-block range. |
| `reference/view4-aerial` | 16:9 | `prompt-v4-aerial.txt` | From high in the north-east: the Loom House in front, bridges to the Hearth House (right) and the Watch Tree (left, lookout at its top), the Seed Tree far back. | The forest floor is drawn as deep ravines. §4.1 has a gentle walkable floor with at most a 1-in-2 slope. |

The plan-view call returned two images. The second (not kept) was an unrequested eye-level picture and is not part of the series. The call may have billed for both.
