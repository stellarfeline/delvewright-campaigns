# The whole-map reference — one prompt and one image per view

The whole-map reference is **five images, one view each**, at the full output
size the provider gives: a front elevation from the shore, the west elevation,
an overhead site plan carrying the player's route, a three-quarter aerial, and
a south–north cutaway section. `tools/refimg.py` runs each prompt unchanged.

The prose all five draw is [`map-brief.md`](map-brief.md); where each zone sits
is [`map-zones.md`](map-zones.md).

## The method, and what it does and does not guarantee

**One view per image.** A view is worth the detail it is drawn at, and four views
divided into one canvas each get a quarter of it. One view per image also makes
the unit of judgement right: a view that comes out wrong is re-drawn on its own,
and the other four are untouched.

**View 1 is drawn from the prompt alone and is then confirmed for style. Views 2
to 5 are drawn from their own prompt PLUS view 1 as a reference image.** These
models anchor on images, and `--style-ref` is the anchor.

**Every later view anchors on view 1, never on the view before it.** Chaining
view to view compounds drift; anchoring all four on one image bounds it.

The trade is stated here so it is checked rather than discovered. Drawing four
views inside one canvas is what makes them agree about the subject's *geometry*.
Drawing them one at a time guarantees only *style*. So **the geometry lives in
the written brief**, and every view is checked line by line against that text
rather than by eye. The check is the table in *What each view agrees with, and
where it does not*, and a view that disagrees is recorded disagreeing.

## Files

| file | what it is |
|---|---|
| `map-style-note.txt` | the series style contract, passed as `--style-note` to every view |
| `map-prompt-v1-front-elevation.txt` | prompt of record for view 1 |
| `map-v1-front-elevation.jpg` · `.json` | **view 1** and its full provider response |
| `map-prompt-v2-west-elevation.txt` | prompt of record for view 2 |
| `map-v2-west-elevation.jpg` · `.json` | **view 2** and its response |
| `map-prompt-v3-site-plan.txt` | prompt of record for view 3 |
| `map-v3-site-plan.jpg` · `.json` | **view 3** and its response |
| `map-prompt-v4-aerial.txt` | prompt of record for view 4 |
| `map-v4-aerial.jpg` · `.json` | **view 4** and its response |
| `map-prompt-v5-section.txt` | prompt of record for view 5 |
| `map-v5-section.jpg` · `.json` | **view 5** and its response |
| `map-prompt.txt`, `map-sheet.jpg`, `map-sheet-alt.jpg` + responses | the earlier four-panel sheets, kept |

Every prompt file is self-contained: it carries the whole subject description, so
`--prompt-file` alone reproduces the request. An approved reference that lives
only in a gitignored working directory is invisible to every later round, so
these are committed.

## The commands

Run from the **pipeline repo root** (that is where `tools/refimg.py` and
`delvewright.local.toml` live). `$C` is this content repo and `$R` is
`$C/campaigns/the-drowned-bell-r2/design/reference`.

View 1 — the prompt alone, plus the campaign's three exterior concept images as
the style anchor. The concept set is the campaign's only inherited material and
the style of record, so the whole-map reference is drawn in its hand:

```sh
python3 tools/refimg.py \
  --prompt-file "$R/map-prompt-v1-front-elevation.txt" \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z7-bell-tower.jpg" \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z0-barrow-shore.jpg" \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z3-drowned-ward.jpg" \
  --style-note "$(cat "$R/map-style-note.txt") The three attached images are approved concept art of parts of this same place. Match their painted hand exactly: visible brushwork, soft atmospheric depth, cool blue-grey cast, painterly edges. Do not draw in a flat graphic or vector-illustration style." \
  --out .refimg/bell-map-v1-front-elevation
```

Views 2 to 5 — the same command shape, anchored on view 1 and on nothing else:

```sh
for v in v2-west-elevation v3-site-plan v4-aerial v5-section; do
  python3 tools/refimg.py \
    --prompt-file "$R/map-prompt-$v.txt" \
    --style-ref "$R/map-v1-front-elevation.jpg" \
    --style-note "$(cat "$R/map-style-note.txt")" \
    --out ".refimg/bell-map-$v"
done
```

**No `--seed`.** The series is drawn on `gemini-native`, whose anchor is the
reference image. Aspect ratio and image size come from the `[refimg]` block of
the gitignored `delvewright.local.toml` (`16:9`, `2K`) and there is no flag to
override them per view, so all five views are 16:9 — which suits an elevation, a
plan and a section equally.

Each interaction id is recorded in that view's `.json`, so any view can be
extended later with `--chain-from` without re-deriving the anchor.

## The style confirmation, and why view 1 was drawn twice

The first view 1 was drawn from the prompt and the style note with no image at
all. It obeyed the brief and it was in the right palette, and it was in the wrong
*hand*: flat, graphic, hard-edged, next to a concept set that is painted, soft
and atmospheric. That is what confirming a view for style is for. View 1 is
therefore drawn a second time with the three exterior concept images as its
anchor, and the second is the view of record and the anchor for views 2 to 5.

The two exterior facts the first drawing carries and the second drops — the
sea-torn breach in the gatehouse's outer wall, and the collapse hole in the upper
ward's paving — are both drawn by views 4 and 5, so nothing is lost by preferring
the hand.

## What each view agrees with, and where it does not

Checked against `map-brief.md` and `map-zones.md` as text, not by eye.

| view | agrees | disagrees with the written geometry |
|---|---|---|
| 1 front elevation | five bands stacked; gate front squat, wide, pale, one arched opening; drowned ward's broken toothed wall with the water-gate tower's peaked roof over it; cloister arcading with open arch-heads; hall roof the one solid dark shape; tower clear of everything, square, unbuttressed, belfry open with the bell nearly filling it; one sea plane; fog closing the frame | **the cut road does not appear on the west cliff**, though the prompt asks for it in full — the same omission the earlier four-panel sheets have. The gatehouse sits on the sand rather than 3.7 m above it, so the portcullis shortcut has no drop in it. The collapse hole is not drawn |
| 2 west elevation | **the cliff road is drawn, and drawn as a route**: a continuous cut ledge crossing the whole face, one body wide, with the bracket line above it, the two rope-store mouths, and its north end turning into the rock at a broken wall-head — which is what the brief needed and what no earlier image had | the K2 gap — the fallen section of shelf at a blind bend — is not drawn, and the brackets are merely irregular. The road's south end fades into the rock instead of meeting the sand. The cliff's foot is drawn as dry sand rather than surf and rock teeth |
| 3 site plan | a true straight-down plan, no horizon and no perspective; the route as one line, solid in the open and dashed under the rock, running the arrival order; large sand flat with cairns and the stake line; cloister as an open court with four ranges; **the ward's east wall torn open so the ward and the sea are visibly one body of water**; causeway to the water-gate tower; collapse hole; tower clear at the crown | two of the nine numbered discs are duplicated (`3` and `9`); none is skipped. A branch of the route line runs from the wake point straight to the gate front, which is the shortcut and not the arrival |
| 4 aerial | the compact stepped mass, every step readable above the last; gatehouse low at the south foot; **the ward as a sunken basin below the gate sill, its curtain wall broken and its east side open to the sea**, arcade in the water, sunk boats, water-gate tower; upper ward with the collapse hole; tower clear on the crown; the cliff road as a line on the west face; fog on every edge | the cloister reads as an L of terraces rather than four ranges round a garth. The cobbled ramp between the collapsed low buildings is not drawn. The sand flat is a band at one corner rather than the flat the brief sizes |
| 5 section | one sea line straight across the frame; sand at −1.2; gatehouse cut open with the passage, its floor channel and its portcullis; **ward floor below the gate sill, filled to the line, causeway just above it**; cloister at +9 roofless; hall at +12 under timber trusses; upper ward at +14 holed; belfry at +30 with the bell built in and a stair climbing the whole tower, broken low down; **the cistern beneath the upper half of the rock, brick barrel vaults on ranked piers, the collapse shaft rising to the hole above it, the well going down to its silt bed** | the tower is drawn between the hall and the cloister rather than set back north of the hall on the crown. The cistern's supply channel is not drawn. The view carries level annotations the prompt forbids; they are correct against `tide.md` except a `+11.0` that names nothing in this campaign |

**The site plan is drawn twice, and the second prompt is the one of record.** The
first asked for thirteen numbered stops and got a plan whose numbering skipped
two and repeated three, a sand flat reduced to a margin, and a drowned ward
drawn as an enclosed pond — which `tide.md` forbids outright, since nothing on
this rock holds a level of its own. The second prompt is a different request, not
the same request run again: nine stops instead of thirteen, an explicit demand
that each number appear exactly once, an explicit size for the flat, and an
explicit statement that the ward's east wall is torn open. All three defects are
answered and the numbering defect is reduced rather than removed.

## What the reference asks for that the grammar plainly cannot build

Named, not redrawn out. A reference that asks for the impossible is a triage
item; quietly simplifying it is how over-simplification arrives through the front
door.

- **The rock itself.** Every view draws a natural crag: curved shoreline, an
  undercut sea cliff, sloping turf shoulders, a rubble talus. The box-split
  grammar has no smooth curve, no diagonal, no noise and no terrain, by design.
  The crag is in-house generator work or a surround layer, and it is not a
  grammar program. It is the largest single thing in the reference and it belongs
  to no zone.
- **Curved and angled walls.** In the plan the ward's ring wall is a curve and
  the sea-wall arm meets the water at an angle; in the aerial the curtain wall
  follows the rock's edge. Curves and diagonals are outside the grammar in the
  same way the crag is.
- **The cut ledge on a vertical face.** View 2 draws the road as a lip
  projecting from the cliff over an undercut drop. `GENERATION.md` records that
  the produced Z1 cannot make that: its one lever lays its course across the
  whole gulf width, so the lip's projection and the drop's width are the same
  number, and the zone ships flush. The road in view 2 is therefore a statement
  of intent that the current program refuses.
- **The bracket line and its rail.** Views 2 and 4 draw the rusted iron brackets
  along the road. `GENERATION.md` records that they have no role and no rule in
  the Z1 program, and beat 1.2 is built on them.
- **The cistern's ranked brick vaults.** View 5 draws round-headed barrel vaults
  on piers. A stepped arch is one recursion in the grammar and reads correctly at
  playable scale, so this is a note about how it will look rather than a blocker.
- The hall's pitched roof, the water-gate tower's pyramid roof, the gate arch and
  the belfry's square opening are all expressible.
