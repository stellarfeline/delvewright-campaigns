# The whole-map reference — how the four views are made

Halgrave's whole-map reference is **four separate images**, each one full-frame:
a front elevation from the causeway head, a side elevation of the west seaward
face, a straight-down site plan, and a three-quarter aerial. Each is generated on
its own, at the whole of the image budget, so a view that comes back wrong is
re-rolled by itself and its three neighbours are untouched.

The prose the four draw is [`map-brief.md`](map-brief.md), and the zone-by-zone
placement is [`map-zones.md`](map-zones.md). It is a prompt, not a feature:
`tools/refimg.py` runs it unchanged.

## Files

| file | what it is |
|---|---|
| `map-view1-front.jpg` | **front elevation**, from the south, from the tidal flat at the causeway head |
| `map-view2-west.jpg` | **side elevation**, the west seaward face, from open water |
| `map-view3-plan.jpg` | **site plan**, straight down, north at the top |
| `map-view4-aerial.jpg` | **three-quarter aerial**, from high to the south-west |
| `map-viewN-*.txt` | the complete prompt of record for that view — `--prompt-file` reproduces it exactly |
| `map-viewN-*.json` | the provider response kept beside the image, and where that view's interaction id is read back from |
| `map-prompt.txt` | the text common to all four: the subject, the six ground planes, the silhouette, the drawing contract |
| `map-style-note.txt` | the system instruction, held constant across the series |

Each `map-viewN-*.txt` is its own camera paragraph followed by the whole of
`map-prompt.txt`, so it stands alone. A fifth view is written by putting a new
camera paragraph in front of that same shared text.

An approved reference that lives only in `.refimg/` is invisible to every later
round, which is how a previous round of this campaign went blind. These are
committed for that reason.

## The order the four are generated in, and why it is not free choice

**View 1 is generated from the prompt alone.** Nothing anchors it: no reference
image, no chained interaction. It is confirmed for style first, because it is
what the other three will be drawn to match.

**Views 2, 3 and 4 are each generated from the prompt plus view 1**, by chaining
on view 1's interaction id — every one of them on *view 1*, never on the view
generated before it. Chaining view to view compounds drift; chaining all three to
one anchor bounds it.

The trade this makes is named rather than discovered. Views co-generated inside a
single canvas agree about the **geometry** of the subject because they are drawn
in one act; views generated in sequence agree only about **style**. So every
geometric fact lives in the written text of every view — the compass, the six
floor heights against the standing tide, the ward's four-metre drop below the
gate, the sixteen metres of blank tower wall — and each returned image is checked
against `map-brief.md` fact by fact, in text, rather than eyeballed against its
neighbours.

## The commands

Run from the **pipeline repo root** (that is where `tools/refimg.py` and
`delvewright.local.toml` live); `$C` is this content repo and `$R` is
`$C/campaigns/the-drowned-bell-r2/design/reference`.

View 1, unanchored:

```sh
python3 tools/refimg.py \
  --prompt-file "$R/map-view1-front.txt" \
  --style-note "$(cat "$R/map-style-note.txt")" \
  --out .refimg/bell-map-view1
```

Views 2, 3 and 4, each anchored on view 1 — the id is `id` in
`map-view1-front.json`:

```sh
python3 tools/refimg.py \
  --prompt-file "$R/map-view2-west.txt" \
  --chain-from "v1_ChdXdTJJYXJhakVvLXYxTWtQd2JPYXlRaxIXV3UySWFyYWpFby12MU1rUHdiT2F5UWs" \
  --style-note "$(cat "$R/map-style-note.txt")" \
  --out .refimg/bell-map-view2
```

`--prompt-file` strips the file's trailing newline, so a prompt file is one
character longer than the string the provider records; nothing else differs.

**No `--seed`.** The configured provider is `gemini-native`, which anchors on
reference images and interaction ids and has no seed; the tool refuses the flag
rather than silently dropping it, which is correct and costs a run.
`--style-code` is likewise not available on this provider.

## The frame each view gets

One image per view exists so that each view gets the frame its subject wants
instead of a quarter of somebody else's. The aspect ratio comes from
`[refimg].aspect_ratio` in the gitignored `delvewright.local.toml` — the tool has
no flag for it — so reproducing a view means setting that key to the value in the
table before the call. `image_size` is `2K` for all four.

| view | aspect | pixels | why this frame |
|---|---|---|---|
| front elevation | `16:9` | 2752 x 1536 | the recognition view is five horizontal bands stacked; a wide frame is what lets them separate, and the tower carries its dominance by being twice the height of the rest rather than by frame headroom |
| west elevation | `16:9` | 2752 x 1536 | the same frame as the front on purpose: the seaward face is the crag's long face, and holding the ratio equal lets the two elevations be read side by side against the same heights |
| site plan | `1:1` | 2048 x 2048 | the crag is an oval whose long axis runs diagonally south-west to north-east, so no rectangle favours it; a square spends the least frame on empty sand and open sea, and the plan is the view a composition program is written from, so pixels on the island matter most here |
| three-quarter aerial | `4:3` | 2400 x 1792 | an oblique of a compact mass needs ground extent and the tower's full height at once; a wider frame either crops the tower or shrinks the whole rock into the middle third |

Four views at 16.95 megapixels together, against 4.23 for a whole four-panel
canvas: each view carries four times the resolution it would as a quarter.

## What the reference asks for that the grammar plainly cannot build

Named, not redrawn out. A reference that asks for the impossible is a triage
item, and quietly simplifying it is how over-simplification arrives through the
front door.

- **The rock itself.** All four views draw a natural crag: a curved shoreline, an
  undercut cliff, sloping turf shoulders. The box-split grammar has no smooth
  curve, no diagonal, no noise and no terrain, by design — so the crag is either
  in-house generator work or a surround layer, and it is not a grammar program.
  This is the largest single thing in the reference and it belongs to no zone.
- **Curved walls.** In the plan the ward's ring wall and the outer sea-wall arm
  are curves, and the causeway meets them at an angle. Curves and diagonals are
  outside the grammar in the same way the crag is.
- **Arch heads.** The cloister and ward arcades are drawn with smooth pointed
  arches. A stepped arch is one recursion in the grammar and reads correctly at
  playable scale, so this is a note about how it will look, not a blocker.
- The hall's steep pitched roof and the water-gate tower's pyramid roof are a
  gable and a spire, and both are expressible.

## Where the four views disagree, and what is not drawn

Four independently generated views of one crag disagree somewhere, and naming
where is worth more than a set that looks tidy. `map-brief.md` and `map-zones.md`
are the authority wherever they do.

- **The water-gate tower is absent from the aerial.** The front elevation, the
  west elevation and the site plan all carry it; the aerial does not draw it at
  all. The plan is the view its position is taken from.
- **The tower's compass position on the crown differs.** The plan puts the bell
  tower on the north-west of the crown with the ramp running to it from the
  east-north-east; the aerial puts it east of the hall with the ramp climbing
  north-east. `map-zones.md` fixes the ramp as climbing north-east and the tower
  as standing north of the hall.
- **The water-gate tower sits on the ward's south-east corner** in the plan;
  `map-zones.md` puts it at the far north-east.
- **The aerial is drawn at a lower water state** than the other three. The
  elevations and the plan are at the standing tide, `0.0`, where the flat is
  awash; the aerial's sand is out of the water.
- **Heights in the elevations are not to scale.** They are silhouette drawings:
  the west cliff reads two to three times taller against the tower than the
  massing table's floors allow. The table in `map-brief.md` is the authority for
  every height; nothing is measured off these images.
- **The cistern is not drawn**, and is not asked for: it has no exterior. Its
  above-ground evidence is the collapse hole in the upper ward's paving, which
  the plan and the aerial both carry, and the grille in the ward's rock face,
  which the aerial carries.
