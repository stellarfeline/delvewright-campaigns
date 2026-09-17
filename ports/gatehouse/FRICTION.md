# Friction — what writing this drawing was actually like

Kept while working, not from memory. One entry per thing that cost time,
surprised me, or was better than expected. Evidence for ADR-0030 §7 and
spec-0072 §§7, 13.

## Convergence

| push | differ | what went in |
|---|---|---|
| 1 | **0** | the whole building, written once |

`30240 cell(s) compared, 0 differ` on the **first execution of the finished
document**. There is no convergence curve to show, and that is the single most
surprising thing about the round. I had budgeted several rounds of
diff-and-repair.

What made it possible: every operation is a box in one frame — the place's own
— so each one can be checked against the generator's column function by hand
before it is ever run. There is no coordinate arithmetic to get wrong, because
there is no arithmetic. The document contains **zero `Expr` objects**.

The comparison is not vacuous: moving one operation (the guardroom brazier's
fire, one cell east) takes the same diff to `2 differ`, exit 1, naming both
cells and both states.

## What the medium did not have

### Set membership on one axis

The single largest cost in the document. The generator writes

```python
if x == 67 and z in (35, 36, 37, 40, 41, 42, 45, 46, 47):
```

— nine cells in one line. A drawing has to notice that this is three runs of
three at stride five and write a `repeat`, which works; but where the set is
not an arithmetic progression there is no arranger at all and the author writes
one box per cell. `z in (34, 43)`; `x in (69, 74, 78)`; the nine parapet
lanterns; the four corner legs of a round table.

**101 single-cell boxes, 4 699 bytes — a quarter of the whole document.**
`repeat` has `count`/`step` and `stride`/`item`; a third spelling that takes a
list of offsets would collapse most of them, and would be the same construct
asked the same question.

### A `mark` cannot name its own cell

Every other operation carries `from`/`to`. A `mark` does not: it takes the
scope it stands in, so naming one cell costs a `scope` wrapper around it.
**8 of them, 989 bytes.** The `offset` form is longer still, because its `x`,
`y` and `z` are `Expr` rather than `Int`, so three tagged objects replace three
integers. Giving `mark` a `from` like everything else would save about a third
of that and one level of nesting.

The `auto` index earned its place: the six muster cells down the passage's
centre line are one `repeat` of one `mark`, not six declarations.

### A role that must be declared and paints nothing

The shell's palette carries three weighted roles; the gatehouse's box paints
two of them. An undeclared `--role` is refused rather than ignored, so to run
the port under the *same* three overrides as the reference the document has to
declare `cobble` — **145 bytes of dead text**. The engine reports a silent
*operation* by address, which is right; it has no way to see a dead *role*, and
under ADR-0030 §5 a fit-out inherits the plan's palette, so this will be normal
rather than rare.

### The priority list has to be inverted by hand

The generator's early `return`s are a priority order: the fireplace beats the
screen, which beats the gallery, which beats the table, which beats the
matting. A drawing has the opposite convention — last wins — so the author
reads the list backwards and paints general before particular. That was easy
and it reads well.

It is not free, though. One case needed an operation that exists only to undo
an earlier one: the duchess's ceiling beams run the room's whole width, but no
beam crosses the second flight's well, so a general `repeat` of `beam` is
followed by a `repeat` of `air` over three cells of it. In the generator that
exclusion is invisible — the flight's branch simply returns first. In the
drawing it is a line of the document, and a reader has to hold it. This is the
honest cost of "later overwrites earlier" and I would pay it again.

### Nothing else

Everything in this building was sayable. spec-0072 §7 predicted that **no
function of `castle/gatehouse.py`** would be among the rows it cannot say, and
that held at every operation: no positional hash, no read of a neighbouring
cell, no float. I never wanted a loop the medium does not have, and I never
wanted arithmetic — the one place I expected to (three doglegged flights whose
tread heights are `15 + (44 − z)`) turned out to be a `prism` and a `repeat`
with a vertical step, with no number computed anywhere.

## What the engine did not tell me

### A malformed operation is addressed at `/`

Dropping `"at"` from every mark gives

```text
error: DW0100: …/no-at.json is not a drawing: missing field `at` at line 3130 column 2 — at /
```

Known at this revision, and being fixed elsewhere. Worth recording anyway:
serde's `line 3130 column 2` **did** locate the file position even though the
operation address is `/`, so a bisect was not needed. The two halves of the
message disagree about how much the engine knows.

### `at` is required on a `mark`

Not friction so much as a surprise: `floor_center` reads like the obvious
default for a one-cell scope, and it is the only thing the released program
ever writes. Nine `mark` declarations, which produce the fourteen anchors, at
18 bytes each.

### `delvec fmt` is not for this document

The manual says a drawing may be run through `fmt`. It should not be. The
hand-laid document is 462 lines and 28 986 bytes; formatted it is **3 285 lines
and 50 633 bytes**, one integer per line, keys alphabetised — so `"op"` sits
after `"note"` and `"from"`, and a reader cannot see what an operation *is*
until its seventh line. The blank lines that separate the storeys go too.
Canonical form is the right answer for a document whose diffs matter and whose
order is semantic; a drawing is a document whose *shape* matters. The two
conventions are in conflict and the drawing loses.

### I never read engine source

Worth stating because the brief asked. Everything the document needed came
from `docs/reference/drawing.md` and `delvec schema --stage drawing`. The
schema export answered every question the manual left (`Sides`, `Section`,
whether `to` may be omitted, which fields are required on which verb) and is a
better reference than the manual for exactly those.

## Instruments I had to write

Read-only. Neither authors nor edits `drawing.json`; both live in the engine
worktree's `target/port/`, not here.

| instrument | why the engine's own verbs were not enough |
|---|---|
| `slice.py` (≈170 lines) — reads a tile-set manifest and its `.nbt` files, prints a column listing (`x,z →` runs of block state up `y`), an `xz` layer at one `y`, or a cell dump | **The engine has no verb that shows you a piece.** `prefab diff` names "the first few" differing cells, which is the right shape for a near-miss and the wrong shape for reading a reference you are about to reproduce. ADR-0030 §7 promises "a sliced view of any sub-box"; at this revision it does not exist. I used it to confirm two columns of the envelope after deriving them by reading the generator — as a check, not as a source. |

That is the whole list: one program, used twice.

## What was pleasant, or faster than expected

- **`faces` with `t`.** The best thing in the medium. "Both walls of the gate
  passage, eight courses, the whole depth" is one operation; the generator
  needs a branch on `x == px0 - 1 or x == px1 + 1` and a separate one for the
  doors through it. Used 12 times, and every one of them replaced two
  operations or a predicate.
- **`prism` with `sides`, and `repeat` with a vertical step.** Between them
  they are a flight of stairs: the masonry wedge and the treads on top of it.
  Three doglegged flights, including their landings and their whole-masonry
  outer columns, are 8 operations. The generator needs a `tread` helper, an
  `edge` predicate and three branches with hand-computed tops.
- **`prism` with `skin`.** The garret's two-course stepped gable is exactly two
  of them, one nested inside the other's footprint. The generator computes it
  per column from `min(z − gz0, gz1 − z)`.
- **`mirror`.** Real work four times: the two fronts' merlons, their arrow
  loops and their windows are one operation each rather than two, and the great
  double hearth is written once and reflected.
- **Derived stair shape.** The generator writes `shape=straight` into three
  palette states and carries a `settle_stairs` pass to repair what that gets
  wrong. The drawing writes no shape at all, and the gate reports 31 stairs,
  every one matching what vanilla derives. `DW0801` is genuinely unreachable
  from here.
- **The report on every run.** `263 operation(s) written · 407 instance(s)
  executed · 16312 cell(s) painted · 13892 surviving · silent: none` is the
  first thing I read after each execution, and "no written operation did
  nothing" is a real check on a document written by hand.

## Two counts worth handing back

- **Six of the thirteen operations built a designed building**: `box`,
  `prism`, `repeat`, `mirror`, `scope`, `mark`. Unused: `cylinder`, `sphere`,
  `pyramid`, `line`, `use`, `grammar`, `claim`. Some of that is this building
  (a rectangular gatehouse has no dome); `use` and `claim` are not — see below.
- **Zero `define`s.** I looked for repetition worth naming and did not find it.
  The building's repeats are strides and reflections, which `repeat` and
  `mirror` say directly; its rooms are each unique. The one candidate — "three
  torches down a wall at stride five", six times — measures the same either
  way, because a `use` costs what the `repeat` it replaces costs. A `define`
  would start paying at a building with several identical bays or towers, which
  this is not. ADR-0030 §3's claim that `define`/`use` is what the generator
  used Python *for* is not contradicted; it is simply not exercised by this
  building, and criterion 10 therefore tests less of §3 than it looks like it
  does.
