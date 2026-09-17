# The gatehouse, drawn

ADR-0030's experiment, first half (spec-0072 criterion 10). One building of
the released castle — the gatehouse — authored a second time as a **drawing**:
a palette and an ordered list of solids the engine executes, written by hand as
a document. No script, generator or template expander produced or edited
`drawing.json`. This directory is not a campaign and imports nothing.

The building is the box `x 65..91, y 0..55, z 30..49` of the released piece —
27 × 56 × 20 cells, 30 240 of them. The drawing is written in that box's own
frame, so local `x` is castle `x − 65` and local `z` is castle `z − 30`.

## What is here

| file | what it is |
|---|---|
| `drawing.json` | the building |
| `sentinels.json` | the single block each weighted role is rebound to for the comparison |
| `measure.py` | is the drawing shorter than the generator's share? (standard library; reads the generator as text, executes none of it) |
| `README.md` | this |
| `FRICTION.md` | what writing it was actually like — a deliverable of equal weight to the diff |

## The instruments

- `delvec` built from the engine at `e6df058f3cd9e387b2463ba78cb73fcd65639e88`
  (`cargo build --release -p delvec`), reporting `delvec 1.6.0, dsl 0.30.0,
  mc 1.21.11`.
- This repository at `73182027db05e14d3a52a39e0c30fabd9025b9c0`, which is the
  revision the released piece and its program are read at.

Set them up once:

```sh
DELVEC=<engine worktree>/target/release/delvec
C=<this repository>
PROGRAMS=$C/campaigns/doune-castle-tour/design/programs
OUT=<a scratch directory outside this repository>
```

## Step 1 — the instrument check

Does re-expanding the released program reproduce the shipped piece? The
provenance row on `prefabs/doune-castle.json` records seed 1 over a
104 × 56 × 120 region.

```sh
$DELVEC grammar expand --file $PROGRAMS/castle.json --region 104x56x120 \
  --seed 1 --id ref-castle --out $OUT/ref-castle --prefabs $C/prefabs

$DELVEC prefab diff $OUT/ref-castle/ref-castle.json $C/prefabs/doune-castle.json \
  --prefabs $C/prefabs
```

```text
698880 cell(s) compared, 0 differ
31 point anchor(s) in the box, 0 differ
```

The instrument reproduces the released piece byte for byte, so the criterion's
fallback (rebuilding the engine revision the campaign pins) is not needed.

## Step 2 — the reference

The same expansion, with **every weighted role of the program** rebound by
`--role` to the distinct single block `sentinels.json` names for it, so no
cell's identity depends on a draw.

| | count |
|---|---|
| weighted roles in `castle.json`'s palette | **3** (`cobble`, `roof`, `wall`) |
| `--role` overrides applied | **3** |

```sh
$DELVEC grammar expand --file $PROGRAMS/castle.json --region 104x56x120 \
  --seed 1 --id ref-gatehouse --out $OUT/ref --prefabs $C/prefabs \
  --role cobble=minecraft:emerald_block \
  --role roof=minecraft:diamond_block \
  --role wall=minecraft:gold_block
```

## Step 3 — the port, and the comparison

The drawing is executed under the same three overrides. `delvec drawing
execute` is the only command that builds it; this directory holds no other
executable but `measure.py`, which reads and prints.

```sh
$DELVEC drawing execute $C/ports/gatehouse/drawing.json --region 27x56x20 \
  --id port-gatehouse --out $OUT/port --prefabs $C/prefabs \
  --role cobble=minecraft:emerald_block \
  --role roof=minecraft:diamond_block \
  --role wall=minecraft:gold_block

$DELVEC prefab diff $OUT/ref/ref-gatehouse.json $OUT/port/port-gatehouse.json \
  --box 65,0,30,91,55,49 --prefabs $C/prefabs
```

```text
30240 cell(s) compared, 0 differ
14 point anchor(s) in the box, 0 differ
```

**The executed drawing's blocks equal the generator's blocks cell for cell
inside the building's box, and the fourteen point anchors inside it agree by
name, cell and facing.**

The comparison binds to the document. Moving one operation — the guardroom
brazier's fire, one cell east — takes the same diff to `2 differ` and exit 1,
naming both cells and both states.

### What `execute` reports

```text
port-gatehouse: pass
  blocks-exist    pass  bound 62      62 block state(s), all present in Minecraft 1.21.11
  shape-complete  pass  bound 59
  states-complete pass  bound 59
  oriented-fills  pass  bound 350
  stair-shape     pass  bound 31      31 stair(s), every written `shape` the one vanilla derives
  non-empty       pass  bound 30240   13892 filled cell(s) of 30240 in the region
  drawing         263 operation(s) written · 407 instance(s) executed · 16312 cell(s) painted
                  · 13892 surviving to the model (0 weighted) · 31 stair(s) settled
  silent          none — every written operation did something
```

`drawing check` reports 263 operations (216 at the top level), 0 defines, 66
roles, 0 params, 0 claimed regions, 9 marks.

**Nothing the engine owns is typed.** The document writes no stair `shape` —
`DW0907` would refuse it, and the 31 stairs (three flights, a garderobe and the
lord's chair) take the shape `derive_shape` gives them. It claims no region:
per criterion 10 that half of ADR-0030's pass condition binds to nothing here,
because the released gatehouse declares no gate — its piece carries 31 point
anchors, no region anchor and no contract.

## Step 4 — shorter?

```sh
python3 $C/ports/gatehouse/measure.py
```

```text
generator, stripped                   14916 bytes   gatehouse.py
drawing, compact, notes removed       19111 bytes   drawing.json
verdict                            NOT SHORTER  (+4195 bytes, 1.28x)

informational
  committed lines                       678 gatehouse.py        462 drawing.json
  committed bytes                     28686 gatehouse.py      28986 drawing.json
  stripped lines                        470
  operations written                    263
  Expr objects (outermost)                0
  Expr bytes                              0 (0.0% of the drawing)
```

**The drawing is not shorter. It is 28% longer.** Both committed numbers in
criterion 10 are correct as the tree has them: `gatehouse.py` is 678 lines and
28 686 bytes.

The strip is cross-checked by a second method that shares no code with it:
parsing the generator with `ast`, dropping every docstring and re-emitting it
with `ast.unparse`, then dedenting, gives 16 573 bytes. `tokenize` gives the
smaller number because `unparse` puts spaces around operators, so the 14 916 the
criterion asks for is the reading least favourable to the drawing, as intended.

Where the bytes are:

| | generator, stripped | drawing, compact |
|---|---|---|
| palette | 3 709 (56 roles) | 4 175 (66 roles) |
| anchors | 264 | — |
| painting / operations | 10 941 | 14 829 (marks included) |
| **total** | **14 916** | **19 111** |

Three readings of that table:

- **The palettes are a wash, and the drawing's own half is smaller.** Of the
  drawing's 66 roles, the 56 the generator declares in `gatehouse.py` cost
  3 390 bytes against the generator's 3 709 — shorter, because the role names
  lose a prefix a place document does not need and two stair states lose the
  `shape` the engine now derives. The other 786 bytes are ten roles the
  generator declares in a shared file; criterion 10 deliberately does not credit
  them, and they are the whole of the palette's excess.
- **42% of the operations is JSON field names.** Of the 14 829 bytes of
  operations, 6 172 are the spellings `"op":`, `"role":`, `"from":`, `"to":`
  and the rest. What the operations actually *say* is about 8 700 bytes against
  the generator's 11 205 of painting and anchors: **the model is more compact
  than the generator; the JSON spelling of the model is not.** spec-0072 §13
  leaves this open for `Expr` alone, where it costs nothing here — the document
  contains zero `Expr` objects. It is the whole document that pays.
- **Nothing in the building was unsayable.** spec-0072 §7 predicted that no
  function of `castle/gatehouse.py` would be among the rows it could not say,
  and that held: every cell of this building is a box, a prism, a mirror or a
  repeat. The excess is spelling, not expressive power.
