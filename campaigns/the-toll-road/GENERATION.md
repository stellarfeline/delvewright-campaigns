# The Toll Road — generation log

First-party mechanic demo, authored via `/new-delve` as deliberate dogfooding
(`docs/demo-levels.md`, row *Traps*). DSL 0.8.0, engine at `cb9c014`.

## Brief (verbatim, owner-approved via the demo-levels queue)

> **The Toll Road** — a short fortified pass where every spec-0011 trap type
> (stair-volley, dart gallery, trapped chest) guards one alcove of loot; disarm
> levers teach counterplay. One mechanic in the spotlight: TRAPS. 10-20 minutes,
> minimum cast (a toll-keeper NPC is plenty), zh-cn as the authored language per
> the shipped-campaign precedent (English canonical strings + zh-cn sidecar via
> the i18n flow).

Constraints carried in from the dispatching session: author at dsl 0.8.0;
happening declarations on story nodes; branch points only if the delve actually
branches; DW0331 caption budget; **no `respawns_on_rest` waves and no bonfires**
(an owner ruling on re-seat semantics is pending — plain checkpoints only,
spec-0012 style); traps use `reset: rearm` per spec-0011 as designed.

## Decisions taken (design)

The full design record is `DESIGN.md`. The decisions that moved away from the
brief, and why:

1. **Three areas, three fixed single-prefab bindings** rather than a jigsaw
   pool. The trap hardware lives in two tidal-keep pieces whose free sockets
   cannot be joined to each other directly (the gatehouse's spare socket faces
   north, the cistern's face west/east), so a pool assembly containing both
   needs at least four pieces plus the courtyard as a linker. Binding each area
   to a single `prefab` gives a fully determined layout, no filler rooms, and
   three legs joined by the compiler's automatic inter-area transport — which
   reads, for a toll road, as three tollgates you cannot walk back through.
2. **The toll-box is empty.** Trap 3 is a `trapped-chest` trigger on the
   undercroft barrel; the loot lives in the secret cell behind it. See finding 2
   and finding 4 — this is the design absorbing a library gap rather than
   pretending it is not there.
3. **The disarm levers are optional counterplay, not gated progress.** See
   finding 5.

## Findings — the dogfooding payload

These are the point of the exercise. Each is a toolchain observation, not a
content workaround.

### Finding 1 — the trap-hardware library is two anchors, on an unmerged branch

The queue's brief assumed a set of spec-0011 trap-hardware prefabs exists. The
library has exactly **two** trap markers, both in the tidal-keep tileset:

| anchor | piece | trigger hardware |
|---|---|---|
| `anchor/l1a-trap-boulder` | `prefab/tk-gatehouse` | `minecraft:stone_pressure_plate` |
| `anchor/l3-trap-darts` | `prefab/tk-cistern` | `minecraft:stone_pressure_plate` |

Neither is on content-repo `main`: the tidal-keep tileset ships with *The
Drowned Bell* (content PR #14, still open). Every other tileset — stone-keep,
cave-shore, island — contains **no** pressure plate, **no** tripwire, **no**
trapped chest and no `anchor/trap` marker at all. A campaign authored on `main`
today cannot declare a single trap.

*Consequence for this delve*: it is branched off `campaign/the-drowned-bell` and
reuses three of its pieces unchanged; the PR is stacked on #14.

### Finding 2 — there is no trapped-chest and no tripwire hardware anywhere

Scanning every `.nbt` palette in the library: `minecraft:trapped_chest` appears
zero times, `tripwire`/`tripwire_hook` zero times, `*_pressure_plate` twice
(the two anchors above). Two of the three trigger kinds in the DSL's
`TrapTrigger` enum therefore have **no hardware to bind to**, and the
player-distinct trigger — the one the spec singles out as the only one a
controlled mob cannot spring — is the one most completely missing.

### Finding 3 — nothing checks that a trap's declared `trigger` matches its hardware

`The Drowned Bell` declares `trap/dart-gallery` with `trigger: "tripwire"` while
the bound anchor's metadata declares
`trigger_block: "minecraft:stone_pressure_plate[powered=false]"` and the piece's
palette contains no tripwire. It builds clean. The trigger kind is load-bearing
for both fiction (what the player sees and learns to read) and semantics
(`trapped-chest` is player-distinct, a plate is not), so a mismatch between the
declared kind and the prefab's `trigger_block` looks like a `DW03xx`-class
validation error waiting to be written. This delve declares
`pressure-plate` on both plate anchors — the honest spelling — rather than
copying the precedent.

### Finding 4 — a `trapped-chest` trap on a container anchor is unproven ground

`emit.rs` summons a `minecraft:interaction` at the trigger cell for a
`trapped-chest` trap with a command payload, and deliberately summons **no**
visible hardware, on the reasoning that "the trapped chest IS the visible
hardware, authored in the prefab". With no trapped chest in any prefab, that
reasoning has nothing to stand on, and two questions are open that no test in
the tree answers:

- does the interaction hitbox **consume** the right-click, so the container
  behind it never opens (making a trapped *loot* chest unreachable)?
- what happens when an `interact` objective and a trap trigger name the same
  anchor — two `minecraft:interaction` entities in one cell? `DW0359`
  (body-eclipse) and `DW0361` (name collision) do not cover it.

This delve routes around both: the toll-box carries no loot and no objective, so
the open questions cannot cost a player the delve. They should be answered by a
PackTest, not by the next campaign that guesses.

### Finding 5 — a disarm is invisible to the critical path, so counterplay cannot be gated

`critical-path.json` has six step kinds — `SelectClass`, `TalkTo`, `Reach`,
`Kill`, `Collect`, `Interact` — and **no step for throwing a trap's disarm
lever**. The harness therefore never disarms anything. The consequence is a real
authoring constraint: an objective gated on a `disarm.sets_flag` would deadlock
the bot even though `analyze` accepts the flag as produced, so **counterplay can
never be made mandatory** in a machine-proven delve. It can only be offered.

That is arguably the right design default (a lever you *may* throw is better
souls design than one you must), but it is currently folklore rather than a
documented constraint, and a campaign that gets it wrong finds out at the bot
stage, not at `analyze`.

### Finding 6 — `tools/i18n-translate.py --reflect` does not exist

The dispatching brief asked for the i18n flow "with `--reflect`". The script's
flags are `--lang`, `--config`, `--delvec`, `--batch-size`, `--dry-run`,
`--force`, `--no-validate`; there is no reflection/critique pass anywhere in
`tools/` or `docs/reference/i18n.md`. Either the flag was planned and not
landed, or the expectation came from somewhere outside the repo — in both cases
`docs/reference/tools.md` is the record that should have settled it and did not.

### Finding 7 — anchor `kind` is dropped from exported prefab metadata

The tileset generator distinguishes `AnchorKind::Container` / `Slot` / plain
(`a_container`, `a_slot`, `a_pos`), and those kinds carry real meaning to an
author: which anchors can hold `loot[]`, which are volley `from_anchor` slots
where nothing stands. The exported `prefabs/*.json` keeps `pos`, `facing`,
`region`, `block`, `dispenser`, `trigger_block` — and drops `kind`. An author
reading the metadata (the only thing the DSL layer can see) cannot tell a
container from a floor cell without reading the generator's Rust source. That is
exactly the layer-boundary folklore CLAUDE.md forbids.

### Finding 8 — `validation/delve-output` is a global path, so worker isolation is partial

`validation/worker-override.yaml` isolates container names and host ports, and
`-p <project>` isolates volumes and networks, but the compose file's build
context is the hardcoded `./delve-output` (only the `packtest` service honours
`$DELVE_OUTPUT`; `server`, `playtest` and `bot` do not). Two workers running
ladders concurrently therefore share the one build tree in the engine checkout:
the isolation story is complete for Docker objects and incomplete for the
artifact under test.

Observed live during this run, which is why it is filed as a finding rather
than a nitpick — at one moment there were **three** worker ladders in flight:

```
$ docker ps --format '{{.Names}}'
dw-worker-wake-bot-1
dw-worker-wake-server-1
dw-worker-tidemill-bot-1
dw-worker-tidemill-server-1
$ cat /private/tmp/delvewright-validation.lock.d/HOLDER
worker-tidemill 1785791153
```

Two of the three were running against the same `validation/delve-output`, and
only one held the mutex. The consequence is that the mutex is not merely
guarding the *host* (ports, container names) as its header says — it is the only
thing standing between two workers and a swapped-out build tree, which means
ladders that `-p` isolation could otherwise run in parallel must be serialised.
The fix that would actually match the stated design is to honour `$DELVE_OUTPUT`
on every service that reads the build, exactly as `packtest` already does.

### Finding 9 — a `collect` objective on a `loot[]` anchor silently destroys the loot

The highest-severity find of the run. `activate_o_<obj>` emits an
**unconditional** `setblock <anchor> minecraft:chest` for a `collect`
objective's prop container, followed by its own `item replace`. If that anchor
is also a `loot[]` target, the prefab's barrel and every stack `setup_finish`
put in it are replaced the moment the objective activates. Captured from a probe
build of this campaign:

```
setup_finish:          item replace block 533 64 38 container.0 with minecraft:book[custom_name=…"The Keep's Toll-Writ"] 1
                       item replace block 533 64 38 container.1 with minecraft:gold_nugget 12
                       item replace block 533 64 38 container.2 with minecraft:golden_apple 1
activate_o_take_writ:  setblock 533 64 38 minecraft:chest
                       item replace block 533 64 38 container.0 with minecraft:book 1
```

Named writ, gold and apple: gone, replaced by one unnamed book. **No
diagnostic.** This is precisely the silent-failure class `DW0431` and `DW0436`
were written for — a `collect.anchor` that appears in `loot[].anchor` should be
an error. Worked around here by pointing both `collect` objectives at standable
anchors *beside* their containers.

### Finding 10 — two `collect` objectives on one item id: the second auto-completes

The emitted per-tick held check is a plain inventory scan:

```
… unless score #party dw.o_take_writ matches 1 store result score @s dw.hold if items entity @s container.* minecraft:paper
```

so a player still carrying the first quest's named paper completes the *second*
paper objective the instant it activates, never having entered the room it is
in. Custom names do not enter the predicate. No diagnostic. Worked around by
giving the two prizes different base items (`paper` and `book`); the honest fix
is either a diagnostic on duplicate `collect` item ids or a name-aware predicate.

### Finding 11 — inter-area transport is keyed on a literal `"spawn"` anchor, and says so nowhere

`plan.rs:1909` looks the destination area's entry up as
`anchors.get(&(next_area, "spawn".to_string()))` — a hard-coded literal, even
though `ENTRY_ANCHOR_NAMES = ["spawn", "entry"]` exists three hundred lines
earlier and its own doc-comment notes that *the island tileset names it
`entry`*. Two consequences:

- an area bound to a prefab with no `spawn` anchor gets **no transport at all**,
  and the failure surfaces as `DW0311` ("the player cannot walk from A to B")
  across a 256-block void — a message that sends you hunting for a wedged
  doorway seam that does not exist. It should detect the area change and say
  *"area `X` exposes no `spawn`/`entry` anchor, so no inter-area transport could
  be emitted."*
- any campaign whose second area is an **island-tileset** piece (which names its
  entry `entry`) silently gets no transport and fails the same way.

Only `tk-barrow-field` carries a `spawn` anchor in the tidal-keep set, so the
first version of this delve — three areas, one fixed piece each — could not be
built. That is what drove the design to a single pooled area.

### Finding 12 — a bare `spawn` anchor in several areas resolves silently, not ambiguously

In the probe where two more pieces were given a `spawn` anchor,
`set-checkpoint {anchor: "spawn"}` resolved to the *gatehouse's* spawn rather
than the barrow field's, with no diagnostic. `DW0305` exists for exactly this
class of ambiguity on pool anchors; the entry anchor is not covered by it.

### Finding 13 — `DW0463` contradicts the documented cast-ledger guidance

SKILL.md tells the author to declare `{at, doing, dialogue}` for **every** cast
entry, and spec-0020 bills `doing` as a forcing function you always fill in.
`DW0463` then rejects exactly that for an `"offstage"` entry, which must be the
bare keyword. Either the skill text or the check should give; today the author
learns it by being red.

### Finding 14 — `DW0351` compares anchor identity, not distance

It fired for an NPC standing at `anchor/l0-reward` `[12,63,20]` while the beat
played at `anchor/l0-reward-cache` `[12,64,21]` — one block apart, both fully on
screen — and reported the exit as *unseen*. The staging it flags is the most
ordinary one there is (a keeper beside his own container). A proximity radius
would be truthful; exact-anchor equality is not.

### Finding 15 — no 1.21.11 client jar on this workstation, so the visual tier cannot run

`delve-render batch` needs the pinned client jar via `--textures` /
`$DELVEWRIGHT_CLIENT_JAR`; the workstation's PrismLauncher has no 1.21.11
instance. The SKILL's step 9 allows skipping with a note, which is what this run
does — but it means every visual claim in this log is from `blocking-chart`
cutaways and in-game inspection, not from rendered frames.

## Rounds

### Round 1 (2026-08-03) — three areas, one fixed piece each

Stages 1–6 authored against the live schema. `validate` and `analyze` clean;
`build` **red on `DW0311`** across a 256-block void between `area/road` and
`area/gate`. Triaged as a **toolchain finding, not a content bug** (finding 11):
inter-area transport is emitted only for a destination area exposing a literal
`spawn` anchor, and only `tk-barrow-field` has one. Proven by patching a probe
copy of the prefab metadata — the identical campaign then built green, twice,
byte-identical. **The patch was not applied to the deliverable**: the metadata is
generator-produced, so a hand-added anchor would not survive regeneration
(ADR-0006) and would carry the library gap forward. The design changed instead.

Diagnostics fought this round: `DW0123` (a `talk-to` with no option that
completes it), `DW0180` (a declared language with no sidecar — see the note on
atomicity below), `DW0463` ×2, `DW0351`, `DW0311` ×2, and in the probe `DW0315`
×2. Findings 9, 10, 12, 13 and 14 all come out of this round.

### Round 2 (2026-08-03) — one pooled area, the road walked end to end

`area/keep` bound to `pool/tidal-keep`. `pieces {min: 6, max: 6}` was rejected by
the compiler's filler arithmetic (`DW0301`); **5/5** is what the pool's socket
geometry admits, and the piece it drops is the bell tower — the one the design
had already put off the road. Accepted as-is rather than fought.

The road grew two connective beats (the wall head and the mustering yard) so the
walk from the gatehouse to the cistern is authored rather than silent, and
Ordwin moved to `anchor/l0-tide-line` so the compiler's `collect` prop chest is
no longer setblocked into the cell he is standing in.

`validate` / `analyze` / `build` all exit 0, zero diagnostics. Double build
byte-identical.

### Round 3 (2026-08-03) — localization

`languages: ["zh-cn"]` and `l10n/zh-cn.json` landed as **one atomic change**:
declaring the language without the sidecar is `DW0180` at validation tier, which
blocks `validate` *and* `build`, so the two are not separable steps however the
workflow is written down.

72 keys, translated by `tools/i18n-translate.py` against the configured
OpenAI-compatible endpoint (2 batches), then **reviewed and repaired in-agent**
— the brief asked for a `--reflect` pass and the flag does not exist (finding 6),
so the reflection was done by hand. Twelve keys were rewritten. The one that
mattered:

> `dlg.ordwin.lever.text` / `fx.first-toll.oc.stair-foot.1.narrate` /
> `fx.last-toll.oc.undercroft-landing.1.narrate` — "the plate **comes out of**
> the floor" had been rendered 从地面**升起** ("rises up from the floor"), the
> opposite of the mechanic. The compiler's flag gate *removes* the trigger block
> (`trap_gate_off_<trap>` clears the cell to air), so a zh-cn player was being
> told the lever arms the trap rather than disarms it. Corrected to 从地面缩回去.

The rest were terminology drift a coverage check cannot see: two spellings of
"the keep" (城寨/城塞), two different renderings of the campaign title in
`world.title` and `area.keep.name`, 关卡 ("checkpoint") used where the sentence
needed the *fee* sense (a 关卡 cannot be 付清), and "Tollwright" flattened to
路税官 ("toll official"), which loses the craftsman sense his whole persona rests
on — 税关匠. **`DW0180`/`DW0181` prove coverage, never fidelity**; a sidecar can
be exactly complete and still contradict the mechanic it describes.

Final: `validate` 0, `analyze` 0, `build` (en) 0, `build --lang zh-cn` 0,
double build byte-identical.

### Visual review

The per-prefab render tier could not run (finding 15 — no pinned client jar on
this workstation). Reviewed instead from `delvec blocking-chart` cutaways: the
critical path is one continuous run from `spawn` west to the demonstration cache,
north through the gate arch, up the gatehouse stair past `anchor/l1a-trap-boulder`
with `anchor/l1a-mural-door` (the disarm lever) on its own landing beside the
run, out along the wall head, across the mustering yard, east into the cistern at
`anchor/l3-landing` with `anchor/l3-dart-lever` and `anchor/l3-gallery-slot`
within a few blocks of the arrival cell, then down the shaft to the alcove and
the secret cell. Both disarm levers are reachable *before* their plates, which is
what makes the counterplay a decision rather than a rumour.
