# The whole-map reference sheet — prompt and command

The sheet is a **multi-view reference**: four views of one place, separated
inside one image — front elevation, side elevation, top-down site plan, and a
three-quarter aerial. It is a prompt, not a feature; `tools/refimg.py` runs it
unchanged.

The prose it draws is `map-brief.md`. The prompt text is
[`map-prompt.txt`](map-prompt.txt), a plain file so `--prompt-file` reproduces
the sheet exactly.

## Files

| file | what it is |
|---|---|
| `map-prompt.txt` | the prompt of record — the text that produced `map-sheet.jpg` |
| `map-sheet.jpg` | **the sheet of record** |
| `map-sheet.json` | its full provider response, kept beside it |
| `map-sheet-alt.jpg` | a second sheet from the same series, kept for one thing it carries better |
| `map-sheet-alt.json` | its provider response — and the anchor id the sheet of record chains from |

An approved reference that lives only in `.refimg/` is invisible to every later
round, which is how the previous round of this campaign went blind. These are
committed for that reason.

## The command

Run from the **pipeline repo root** (that is where `tools/refimg.py` and
`delvewright.local.toml` live); `$C` is this content repo.

```sh
python3 tools/refimg.py \
  --prompt-file "$C/campaigns/the-drowned-bell-r2/design/reference/map-prompt.txt" \
  --chain-from "v1_Chd5Z1NBYXBuNktxR0FfdU1QeHV2bi1BTRIXeWdTQWFwbjZLcUdBX3VNUHh1dm4tQU0" \
  --style-note "Every image in this series is one place drawn in the same hand: muted grey and grey-green desaturated painted concept art, flat cold overcast North Sea light, sea fog, no sun, no cast shadows, massing and silhouette over detail. Obey the requested panel layout exactly, including any panel that is a flat overhead map rather than a view." \
  --out .refimg/bell-map-sheet
```

The `--chain-from` id is the series anchor and it is recoverable only from
`map-sheet-alt.json`, where the provider returned it. The interaction that
started the series was anchored on images instead:

```sh
python3 tools/refimg.py \
  --prompt-file <the same text, with the plan bullet in its first form> \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z7-bell-tower.jpg" \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z0-barrow-shore.jpg" \
  --style-ref "$C/campaigns/the-drowned-bell-r2/design/concept/z3-drowned-ward.jpg" \
  --style-note "…massing and silhouette over detail. Obey the requested panel layout exactly." \
  --out .refimg/bell-map-sheet-alt
```

and its plan bullet read, in full:

> `- BOTTOM LEFT: top-down site plan, a bird's-eye map of the whole island from directly above, north at the top.`

**No `--seed`.** The configured provider is `gemini-native`, which anchors on
reference images and has no seed; the tool refuses the flag rather than silently
dropping it, which is correct and costs a run. `--style-code` is likewise not
available on this provider and is mutually exclusive with `--style-ref` anyway.
Config is `[refimg]` in the gitignored `delvewright.local.toml`; the key is read
from the env var that block names, at call time.

Aspect ratio and image size come from that config (`16:9`, `2K`) and are right
for a 2 x 2 sheet — each panel lands near 8:9, which suits an elevation.

## The three style anchors, and why those three

`--style-ref` takes at most three. The eight concept images are not
interchangeable for this job, because five of them are interiors or close
studies and an interior anchor teaches the model to draw an interior.

| anchor | what it is there to carry |
|---|---|
| `z7-bell-tower.jpg` | the tower, the open belfry, the bell inside it, the cobbled ramp and the collapsed low buildings — the crown of the silhouette and the object the campaign is named after. The only concept that shows a whole building from outside. |
| `z0-barrow-shore.jpg` | the sea, the wet sand, the cairns, the stakes, the fog and the flat overcast light — and the one standpoint the elevations are drawn from, which is the shore looking at the rock. |
| `z3-drowned-ward.jpg` | standing sea water against pale wet ashlar, ruined arcading, and the water-gate tower's peaked metal roof — the drowned band at the foot of the massing. |

Excluded, with the reason: `z1` is a close texture study of a rock face; `z2`,
`z5` and `z6` are interiors; `z4` is an enclosed court seen from inside it.

## What came back

Both sheets returned four panels with clean gutters, one place drawn four ways.
**The multi-view separation survived**: the model did not merge the views and did
not draw four unrelated buildings. That failure mode is not a live risk on this
provider with this prompt, so the queued second-provider answer is not needed
here.

`map-sheet.jpg` is the sheet of record. It carries all four requested view types:
two flat elevations against a sea horizon, a genuine straight-down site plan with
no horizon and no perspective, and a three-quarter aerial. The plan panel is why
it is the one of record — it is the view a composition program would be written
from, and it reads: the sand flat and its cairn field and stake lines to the
south-west, the gatehouse block at the flat's head, the flooded ward as a ring of
water inside a broken wall with the causeway crossing it and the water-gate tower
at its far side, the cloister's open court, the hall's dark roof, the tower, and
the black collapse hole in the ground beside the tower.

`map-sheet-alt.jpg` is kept for one thing the sheet of record loses: **the bell.**
In the alternate the belfry is a square opening on every face and the bell nearly
fills it, which is what `story.md` means by *built, not hung as an ornament*. The
sheet of record draws the belfry as a single arched opening with a smaller bell in
it, and to that extent it under-draws the campaign's central object. The prose in
`map-brief.md` is the binding statement of the bell's scale; between the two
images, the alternate's belfry is the one to build from.

## What the sheet asks for that the grammar plainly cannot build

Named, not redrawn out. A reference that asks for the impossible is a triage
item, and quietly simplifying it is how over-simplification arrives through the
front door.

- **The rock itself.** Both sheets draw a natural crag: a curved shoreline, an
  undercut cliff, sloping turf shoulders. The box-split grammar has no smooth
  curve, no diagonal, no noise and no terrain, by design — so the crag is either
  in-house generator work or a surround layer, and it is not a grammar program.
  This is the largest single thing on the sheet and it belongs to no zone.
- **Curved walls.** In the plan panel the ward's ring wall and the outer sea-wall
  arm are drawn as curves, and the causeway meets them at an angle. Curves and
  diagonals are outside the grammar in the same way the crag is.
- **Arch heads.** The cloister and ward arcades are drawn with smooth pointed
  arches. A stepped arch is one recursion in the grammar and reads correctly at
  playable scale, so this is a note about how it will look, not a blocker.
- The hall's steep pitched roof and the water-gate tower's pyramid roof are a
  gable and a spire, and both are expressible.

## What the sheet does not draw

- **Z1's cut road-ledge does not appear on the west cliff in any panel of either
  sheet**, although the prompt asks for it in both. The west face is drawn as
  unbroken cliff.
- The tidal sand wraps most of the island in the plan panel. `story.md` and
  `tide.md` put the causeway to the mainland on one side only.
- The cistern is deliberately not asked for and is not drawn: it has no exterior.
  Its only above-ground evidence is the collapse hole, which both sheets draw,
  and the grille in the ward's rock face, which neither does.
