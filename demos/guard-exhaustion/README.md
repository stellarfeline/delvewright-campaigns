# Guard Exhaustion

A grammar program that refuses to expand, and **the refusal is the artifact**.

Every other demo here ships a building. This one ships a message, because the
message is the capability: when no alternative of a rule applies, the build says
which comparisons rejected it, what both sides of each one came to, and where in
the derivation the scope came from.

---

## The program

`signal-station` is a three-part piece. A gravel apron across the approach; two
solid flanking blocks; and, in the bay between them, a covered walk with a rail
on each side.

The walk's `plan` rule is authored **in the walk's own frame** — its local `Z` is
the run, counted from the far end. The run happens to lie along world `X`, so the
rule is turned a quarter-turn against the world before it is called.

Three steps reach it:

| step | what it does | the box it hands on |
|---|---|---|
| `station` | splits world `Z`: a 3-block apron, then the terrace | 21 × 9 × 10 |
| `terrace` | splits world `X`: a 5-block flank, the bay, a 5-block flank | 11 × 9 × 10 |
| the bay | is handed to `plan` in the walk's frame | local 10 × 9 × 11 |

`plan` has three alternatives and **no `otherwise`**, so if none of them applies,
the expansion stops.

---

## What it prints

At a region of 21 × 9 × 13 — one block under what the walk needs:

```
$ delve-grammar expand --file signal-station.program.json \
      --region 21x9x13 --seed 1 --id signal-station -o out/
error: signal-station: no alternative of rule "plan" applies to this scope, and none is `otherwise`
  at: station › split z→z piece 2/2 › terrace › split x→x piece 2/3 › plan
  scope: local 10x9x11 (x→world z, y→world y, z→world x, local z reversed; world box corner 5,0,3 size 11x9x10) — these are the dimensions at the failure site, not the region as given
  alternative 1 of 3 rejected — 3 condition(s) decided it:
    required dim:z >= ((param:landing + param:deck) + 5); at this scope left = 11, right = 12  [param:landing = 4, param:deck = 3]
    required (dim:z - param:landing) >= ((param:deck * param:stringer) + 2); at this scope left = 7, right = 8  [dim:z = 11, param:landing = 4, param:deck = 3, param:stringer = 2]
    required dim:smallest > (param:landing + 6); at this scope left = 9, right = 10  [param:landing = 4]
  alternative 2 of 3 rejected — 3 condition(s) decided it:
    required dim:y == param:crown; at this scope left = 9, right = 1
    forbidden (under none_of) dim:x <= (param:landing + 6); at this scope it held, left = 10, right = 10  [param:landing = 4]
    could not evaluate (dim:z / param:flight) >= param:deck: division or remainder by zero
  alternative 3 of 3 rejected — 1 condition(s) decided it:
    required orientation x→x, y→y, z→z; this scope has x→z, y→y, z→x, local z reversed
exit 2
```

The transcript is `refusal.txt`, and it is the one the tool printed.

---

## Reading it

**The scope line is the point of the whole message.** The region typed on the
command line is 21 × 9 × 13. The box the rule is actually looking at is
**10 × 9 × 11**, and not one of those three numbers appears in the command. Two
splits took blocks off two axes, and the turn then swapped which world axis each
local name refers to: the rule's `dim:z` is world `X`, its `dim:x` is world `Z`.
`local z reversed` says the run counts from the far end, which is a different
frame again from one that merely maps the same axes.

Without that line an author has a rule name and nothing else, and the only move
left is to try regions until one works — on the wrong axis, in the wrong units,
with three axes to sweep.

**Alternative 1 lists every conjunct that failed, not the first.** Three of the
five comparisons in its `all` are false here. They are handed over together
because fixing one and re-running only to meet the next is the sweep this message
exists to end. Each carries the expression as it was written, the two values it
came to, and — where an operand is composite — every `param` and `dim` inside it,
so `right = 12` can be traced to `landing = 4` plus `deck = 3` plus 5 without
opening the program.

The third of them reads `dim:smallest`, the shortest side of the box, and its
value is 9: not 21, not 13, and not any number on the command line either.

**Alternative 2 shows the two cases a comparison list alone cannot.** Its
`none_of` is a disqualification — *this alternative is out if the bay is 10
blocks or narrower* — so what gets reported is a condition that **held**, printed
as `forbidden (under none_of)` with the values that made it hold. And its last
conjunct divides by a parameter that is still zero. That conjunct is never
evaluated during the build, because the conjunct before it is already false and
the test stops there; the report walks the guard anyway and names it rather than
leaving a silent hole where a constraint should be.

**Alternative 3 is a frame guard**, and it prints the frame it wanted beside the
frame it got. Both halves are shown — the axis mapping and the reflection —
because two frames can share a mapping and still be different frames.

---

## Checking the arithmetic instead of trusting it

The message claims a boundary: `dim:z` is 11 where 12 is required, and `dim:z` is
world `X` less the two 5-block flanks. So one more block of world `X` should make
the rule apply, and one fewer should make it refuse harder. Nothing else on the
command line should matter.

```sh
delve-grammar expand --file signal-station.program.json --region 20x9x13 --seed 1 --id signal-station -o out/
delve-grammar expand --file signal-station.program.json --region 21x9x13 --seed 1 --id signal-station -o out/
delve-grammar expand --file signal-station.program.json --region 22x9x13 --seed 1 --id signal-station -o out/
```

| region | `dim:z` at the failure site | result |
|---|---|---|
| 20 × 9 × 13 | 10 | refuses — **four** conjuncts, one more than at 21 |
| 21 × 9 × 13 | 11 | refuses — three conjuncts |
| 22 × 9 × 13 | 12 | **passes**, 1902 filled cells, every gate green |

The boundary lands exactly where the message put it. The run one block smaller is
worth reading too: a fourth condition appears, the `none_of` in alternative 1
that only starts to hold below 11. An author who had been handed one constraint
at a time would have met it on the next attempt.

The whole transcript is `boundary.txt`.

---

## What is in this directory

| path | what it is |
|---|---|
| `signal-station.program.json` | the program |
| `refusal.txt` | the refusal at 21 × 9 × 13, as the tool prints it |
| `boundary.txt` | all three runs |
| `signal-station.nbt` | the piece the passing run builds |
| `signal-station.json` | its metadata, and the program hash and seed that regenerate the bytes |
| `signal-station.report.json` | the gate verdicts and measurements of the passing run |

---

## Build it yourself

Everything here comes from `signal-station.program.json` and one tool built from
source. Clone the pipeline repository,
[stellarfeline/delvewright](https://github.com/stellarfeline/delvewright), then,
from its root:

```sh
cargo build --release -p delvewright-grammar --bin delve-grammar
export PATH="$PWD/target/release:$PATH"
```

Then run the three commands above from this directory. The `.nbt` is a pure
function of the program, the region and the seed (ADR-0006): the passing run
rewrites the same 5,875 bytes every time.

---

## What this demo does not claim

`signal-station` is a teaching program, not a piece to build with, and the
passing run says so in three findings rather than leaving them to be discovered:

- **No spatial contract.** Nothing is declared about which space is enclosed or
  which edge is a way in, so every contract obligation over this piece examines
  nothing.
- **Zero entry cells.** The walk is sealed by its own rails and flanks, so the
  reachability measurement has nowhere to start and binds to nothing. The 96
  standable cells inside are counted and reported unreachable, which is the
  honest reading, not a pass.
- **No anchors.** Nothing in a campaign could name a place inside it.

A piece meant for a level answers all three. This one exists so that a rule can
be watched not applying.
