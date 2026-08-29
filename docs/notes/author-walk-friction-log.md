# Walking steps 1, 2 and 3 of `/new-delve` from a clean clone

An observation round. It fixed nothing, edited no page, tool, check or campaign,
and the campaign it wrote was discarded. What it produced is this list.

## What was walked, and with what

A fresh `git clone` of this repository, LFS materialised, and the engine built
from source at the revision `versions.toml` `[engine].authoring_ref` names —
`b65783e8a0ee65e3308c67b52b1e1922dc0b1638`, which reports
`delvec 1.1.0, dsl 0.19.0, mc 1.21.11`. The subject was a throwaway of the
round's own invention, a site-plan campaign of five places, chosen so that
nothing in it could seed a campaign somebody else is going to make.

`Init` -> *Which placement model* -> §1 -> §2B -> §3, then `delvec fmt` and
`delvec validate`. It stopped at §4, whose actor is the user.

**The generator was deliberately not used as the authoring path.** Every
previous walk of this pipeline reached its campaign by running
`delvec metrics --gym`, which writes all nine documents at once. Nothing below
was copied out of it; the two gym commands the placement section prints were
run at the end, to check that they still work.

## Counts

**Commands the page prints across §1–§3** (counting the *Which placement model*
section, which the page places before step 1), deduplicated by form:

| | command | section | outcome |
|---|---|---|---|
| 1 | `delvec metrics --gym .out/gym` | placement | ran, worked as written |
| 2 | `delvec --prefabs prefabs build .out/gym -o .out/gym-out` | placement | ran, worked as written |
| 3 | `delvec schema --stage <name>` | §1, §3 | ran, worked as written |
| 4 | `delvec schema --stage all` | §1 | ran, worked as written |
| 5 | `delvec --prefabs prefabs validate <campaign-dir>` | §1, §3 | ran, worked as written — but see F1 |
| 6 | `delvec metrics > table.json` | §2B | ran, worked as written; 341 lines, the page's own figure |
| 7 | the entry-anchor census heredoc | §2A | not run — §2A is the branch not taken |

**7 printed, 6 run, 6 worked exactly as written, 0 needed an intervention, 1
not run** because it belongs to the other placement branch.

`delvec fmt` and `delvec fmt --check` (§6) were run over the result at the
brief's request: both worked as described — 9 files examined, idempotent on a
second run, `--check` green.

**Init**: about 24 commands printed across steps 0–7. 21 run, 21 worked as
written, 0 interventions. Three were not run: Init 4's two arms, because that
step is a hand-over whose actor is the user, and Init 7, which the page says to
skip unless a custom skin is wanted. The page's own closing checklist —
*Init is finished when every one of these answers* — was run verbatim:
**11 of 11 answered.**

**Consultations outside the page: zero.** No engine source, no spec, no
`docs/reference/`, no existing campaign document was opened to author anything.
`delvec schema` and `delvec metrics` — both named by the page at the step that
needs them — were the whole authority, and they were sufficient: every tagged
union, enum, id format and required field of all nine documents came out of
them.

## Friction

### F1 — §3 cannot end clean, and the page tells you to loop until it does

**The worst item, by how long it stops someone who cannot read the compiler.**

§3 says to run `delvec validate` after each story document, *"fixing by
diagnostic code"*, and adds that *"three failed repairs on the same code means
stop and look at the design"*.

Once the quest plan is written, `validate` reports one `DW0150` per planned
quest — five of five here — and the two remedies it names are:

* add a stage-5 quest with that id, which is **§5**, two steps further on, with
  the design gate in between; or
* drop it from the stage-4 plan, which is deleting the document just authored.

There is no stub available. A stage-5 quest requires `trigger`, `objectives` and
`on_complete`, and the schema-minimal one — a `campaign-start` trigger with both
arrays empty — is refused twice over: `DW0460` once per live NPC per quest,
because a quest must account for every NPC in its `cast`, and `DW0481` once per
quest, because a quest must say what it does to the story. **Measured: writing
the five minimal stage-5 quests moved the error count from 5 to 15** — ten
`DW0460` and five `DW0481` — so the cheapest route past §3's red is
three times worse than the red it was trying to clear.

So §3's loop terminates on an error count equal to the campaign's
quest count, the "three failed repairs" rule fires on a document that is
correct, and the author arrives at §4 — the gate they are told never to fake —
holding a campaign that does not validate. Nothing on the page says that is the
expected state.

The defect belongs to the pair. `DW0150` is right; §3's instruction is right for
the other two documents; their union is unsatisfiable at that point in the run.

### F2 — the `dsl_version` in the envelope example is stale, and not harmlessly

The envelope block prints `"dsl_version": "0.17.0"`. Eleven lines later the page
says to write the number `delvec --version` printed, which is `0.19.0`. The
example is the copyable one.

Measured, on the same nine documents rewritten to `0.17.0`: **two `DW0141`
fences**, on `way_class` and on a seam `contact` — both of them surfaces §2B
itself instructs the author to write. So the consequence is not theoretical and
it lands in the newest part of the pipeline. `delvec metrics --gym`, the page's
own worked example, writes `0.19.0`.

### F3 — the stub recipe is exact for five documents and impossible for the sixth

`DW0874` is an unusually good diagnostic: with only `world.json` on disk it
names every missing document, gives the whole six-name list, and prints the
recipe — *"a stub is that document's envelope and nothing else: `content`
carrying only the fields its schema requires."*

That recipe cannot be followed for `quest-plan.json`. Its schema requires both
`quests` and `finale`, and `finale` must name a member of `quests`; an empty
array is refused by `DW0131`, whose remedy — *"set `finale` to the id of an
existing planned quest"* — cannot be performed without authoring one. The stub
that does work then draws `DW0112` (no area declared yet) and `DW0150` (no
stage-5 expansion), which is two more documents' worth of obligation arriving
during what the page calls stubbing.

### F4 — `DW0110` does not carry the id form for the type it rejected

A dialogue node written `dlg/<npc>/<name>` is refused with *"ids must be
lowercase kebab-case with their type prefix (e.g. `area/keep`, `npc/keeper`,
`quest/find-key`)"*. None of the three examples is a dialogue id, and the actual
rule — `dlg/<kebab>`, exactly one segment after the prefix — is in the schema
description rather than in the refusal. The page does not spell a dialogue node
id anywhere either. One `delvec schema --stage dialogue` away; but the refusal
alone does not name the remedy.

### F5 — §2B's first instruction is a paid account, and this round could not pass it

*"Before any of them: the whole map gets a reference of its own... On path B,
draw it now."* Path B needs a `[refimg]` section in the engine checkout's
`delvewright.local.toml` and a provider key in the environment. On a clean Init
the engine checkout is fresh, so the file does not exist and
`refimg.py --dry-run` exits 2 — exactly as the page promises, with exactly the
message the page promises.

**This round departed from the page here**: it authored the three site-plan
documents with no map reference. That is recorded rather than papered over. For
an author whose design is already approved and sitting in `campaigns/<id>/design/`
this is not friction at all — Init 6 path A is a read. For anyone starting a new
campaign, the first act of §2B costs a third-party account, and Init 6 is where
that becomes visible, which is the right place but easy to defer past.

### F6 — `world.json` is the one document no step tells you to write

§1 lists the filename. §2 is titled *Placement — where everything is*, and 2B
mentions `world.json` only to say its `areas[]` is empty and that declaring two
placement authorities is `DW0839`. But the document carries six required fields
— `title`, `theme`, `premise`, `seed`, `target_minutes`, `areas` — and no step
on the page asks for any of them. One `delvec schema --stage world` settles it.

While there: the schema's own description of `areas` reads *"1..N areas"*, which
contradicts §2B's "empty". §2B is the one that is right, and the page says the
schema is the authority where they disagree — so the one line of the schema that
is prose rather than structure is the one that could send an author the wrong
way.

### F7 — Init 4 is an unconditional hand-over with no look-first clause

Init 6 path A opens with *"Look first"*. Init 0's Java clause argues the general
case explicitly: *"halting for something already present spends the user's
session on a `PATH` line."* Init 4 has no equivalent — it presents both ways the
client jar can arrive and waits, even when the jar is already at
`~/.chunky/resources/minecraft.jar` from an earlier run. It was, on the machine
this walk ran on.

### F8 — the page understates its own diagnostic

§1 says `delvec validate` *"hard-errors on the first one it cannot find, naming
it — so if you do not know the names it will spell them out one run at a time"*.
It does not. `DW0874` names all five missing documents in one run, with the
stubbing recipe attached. Wrong in the safe direction, but it teaches an author
to expect a five-run loop that does not exist.

## What the walk established the page gets right

Worth stating, because a friction list read alone reads as a verdict.

* Every Init command ran as written on a clean clone. The closing checklist
  answered 11 of 11.
* The JDK enumeration loop worked verbatim in `zsh` on a machine whose default
  `java` is 17, and selected the keg-only `openjdk@21` the loop's own comment
  says a path-trusting search would miss.
* The shell-state probe (`export DW_PROBE=1`, then `echo $DW_PROBE` as a
  separate command) behaves exactly as the page predicts for an agent runtime:
  the second command sees nothing.
* Init 3's predicted failure —
  `internal error: cannot read prefabs dir campaigns/prefabs` — reproduces
  character for character, and it is exit 10 wearing the words "internal error"
  exactly as warned.
* The refusals do the teaching. The site plan was accepted on the second
  attempt; its one error, `DW0876`, printed both spans in numbers
  (`64..69 on y, against the face's 69..71`) and three concrete remedies. The
  layout graph, the geometry brief, the NPCs and the classes were each accepted
  first try, from the schema alone.
* Every validation line states its binding count, and states a zero as a
  finding rather than passing over it — the site plan's *"declares no
  whole-owned volume, so the check ... examined nothing"*, and the graph's
  *"no beat ... belongs to a quest the finale depends on"*.
* `delvec fmt` does what it says: nine files, array order untouched, idempotent,
  `--check` green, binding count printed.

## The campaign

Discarded, as the round was told to. Nothing was committed to `campaigns/`.
