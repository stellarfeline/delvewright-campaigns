# The whole-map reference — one prompt and one image per view

The whole-map reference is **five images, one view each**, at the full output
size the provider gives: a front elevation from the shore, the west elevation,
an overhead site plan carrying the player's route, a three-quarter aerial, and
a south–north cutaway section. `tools/refimg.py` runs each prompt unchanged.

The prose all five draw is [`map-brief.md`](map-brief.md); where each zone sits
is [`map-zones.md`](map-zones.md).

## The method, and what it does and does not guarantee

**One view per image.** A view is worth the detail it is drawn at, and five views
divided into one canvas each get a fifth of it. One view per image also makes the
unit of judgement right: a view that comes out wrong is re-drawn on its own, and
the other four are untouched.

**The aerial is the anchor, and it is drawn first from its prompt alone.** Before
anything else is drawn it is gated against `map-brief.md` and `map-zones.md` —
the compass frame and every zone's position, fact by fact. An anchor carries into
all four of the others, so an anchor that is wrong is four wrong images, and a
failing anchor is re-drawn by itself until it passes.

**It is the anchor because it is the only view that carries both layout and
light.** A plan has the layout and no material to match a hand against; an
elevation has the hand and almost none of the layout. A series anchored on an
elevation gives its other views nothing to inherit about where things sit, so
each invents it, and they disagree about the compass.

**Every later view anchors on one image, never on the view before it.** Chaining
view to view compounds drift; anchoring on one image bounds it.

**A reference image fixes layout and hand. It does not fix projection, and it
overrides a view type when the two conflict.** With the aerial attached, the west
elevation, the site plan and the section each came back as the aerial. So each of
those prompts states in its own terms what it is not — a plan carrying a horizon
is wrong, a section showing the island's skin is wrong — and the two orthographic
views anchor on the **front elevation**, which is itself anchored on the aerial.
The layout still descends from the anchor; it descends one step further, through
a view whose projection does not fight theirs.

The trade is stated here so it is checked rather than discovered. Drawing views
inside one canvas is what makes them agree about the subject's *geometry*.
Drawing them one at a time against an anchor guarantees *style*, and as much
*layout* as the anchor shows. So the geometry still lives in the written brief,
and every view is checked line by line against that text rather than by eye. The
check is the table in *What each view agrees with, and where it does not*, and a
view that disagrees is recorded disagreeing.

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

The aerial — its prompt alone, with nothing attached:

```sh
python3 tools/refimg.py \
  --prompt-file "$R/map-prompt-v4-aerial.txt" \
  --style-note "$(cat "$R/map-style-note.txt")" \
  --out .refimg/bell-map-v4-aerial
```

The two elevations — anchored on the aerial and on nothing else:

```sh
for v in v1-front-elevation v2-west-elevation; do
  python3 tools/refimg.py \
    --prompt-file "$R/map-prompt-$v.txt" \
    --style-ref "$R/map-v4-aerial.jpg" \
    --style-note "$(cat "$R/map-style-note.txt")" \
    --out ".refimg/bell-map-$v"
done
```

The plan and the section — anchored on the front elevation, whose projection does
not fight theirs:

```sh
for v in v3-site-plan v5-section; do
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

## What each view agrees with, and where it does not

Checked against `map-brief.md` and `map-zones.md` as text, not by eye.

| view | agrees | disagrees with the written geometry |
|---|---|---|
| 4 aerial (the anchor) | the compact stepped mass, every step readable above the last, with the flat, the gatehouse, the ward, the cloister, the hall, the upper ward, the tower and the collapse shaft all inside one downward look; **the flat awash at the standing tide**, cairns and stakes standing up out of shallow water; **the ward a sunken basin below the gate sill**, its curtain wall broken and its east side open to the sea; **the raised causeway ending at the water-gate tower**, which is square, three-storeyed and pyramid-roofed; the cloister roofless with four ranges round an open court; the upper ward's cobbles holed; the tower clear on the crown, one square belfry opening per face with the bell nearly filling it; the cliff road with its rope-store mouths; fog on every edge | the causeway of wet sand running off south to the mainland is not drawn — only the ward's own raised spine is. One free-standing arcade stands in the water where the brief has two. The grille in the ward's rock face is not drawn |
| 1 front elevation | five bands stacked; the flat awash, cairns and stakes standing in shallow water; gate front squat, wide, pale, one arched opening, roof flat; the ward's broken toothed wall with the water-gate tower's peaked roof over it at the far side; cloister arcading with open arch-heads; the hall's roof the one solid dark shape; the tower clear of everything, far higher than the rest, belfry a square opening with the bell nearly filling it; one sea plane; fog closing the frame | the tower's shaft reads round-shouldered rather than square below the belfry. The gate floor sits at the sand rather than nearly four metres above it, so the portcullis shortcut has no drop in it. The cut road on the west cliff is faint |
| 2 west elevation | **the cliff road is drawn as a route**: a continuous cut ledge crossing the whole face, beginning at the tidal sand at its south foot and ending at a broken sea-torn hole in the gatehouse's outer wall high above the sand, with the bracket line and the two rope-store mouths on it. That is what `map-brief.md` calls a stage of the route rather than a detail of the gatehouse, and this is the view that carries it. Sheer undercut cliff to surf and rock teeth; the flat awash to the south; the water-gate tower's peaked roof over the curtain wall | the bell tower is drawn between the hall and the cloister rather than set back north of the hall on the crown. The K2 gap — the fallen section of shelf at a blind bend — is not drawn |
| 3 site plan | north at the top, the cliff west, the breach east; the arrival route as one line running the arrival order, solid in the open and dashed under the rock; the flat awash with its cairns and its stake line; the cloister an open court with four ranges; **the ward's east wall torn open so the ward and the sea are visibly one body of water**; the causeway ending at the water-gate tower; the collapse hole in the upper ward; the tower clear at the crown with the bell seen down through it | the rock is still drawn with some of its side faces showing rather than as a true straight-down projection. The water-gate tower sits at the ward's south-east, where the aerial puts it at the ward's far side away from the gatehouse |
| 5 section | one sea line straight across the whole frame; the flat at −1.2, awash; the gatehouse cut open with its passage, its floor channel and its portcullis; **the ward floor below the gate sill, filled to the line, the causeway just above it** with sunk boats in the water; the cloister at +9 roofless; the hall at +12 under open timber trusses; the upper ward at +14 holed, with the shaft falling from that hole; the belfry at +30 with the bell built into it and a stair climbing the whole tower; **the cistern beneath the upper half of the rock, brick barrel vaults on ranked piers, and the well going down below the silt line**. All three of the massing's *facts a plan drawn from boxes loses* are carried in this one drawing | the view carries no level annotations, so every height is read from the massing table rather than off the picture. The cistern's supply channel is not drawn |

**The aerial passed its gate on its first drawing; the west elevation, the plan
and the section are each re-drawn alone.** The west elevation is re-drawn because
its frame handedness was inverted: a viewer facing east has north on the left,
which is the same rotation the front elevation applies facing north, and until
that agreed the two elevations could not be read side by side against the same
heights. The plan and the section are re-drawn because, with the aerial attached,
each returned the aerial; a stated refusal naming the wrong answer moved neither,
and what moved them was changing which image they attach.

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
