# The Toll Road — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0011 (traps: stair-volley, dart
gallery, trapped chest) pinned: a short fortified pass where every trap type
guards one alcove of loot, and disarm levers teach counterplay. One mechanic,
small, minimum cast. "Every trap type" was read against the engine that builds
this level: the three trap triggers (`pressure-plate`, `tripwire`,
`trapped-chest`), the two trap payload verbs (`volley`, `collapse`), the
disarm affordance, and the `step` trigger a plate can also carry.

## What was invented here

- The fiction: Harrow Gap, a walled pass whose toll wardens left a generation
  ago; the strongrooms in its walls still trapped; the toll bar at its head
  still down; the party as carters going through.
- Which trap guards which strongroom, in walking order: the toll booth's plate
  carries the harmless `step` trigger (a bell and an actionbar line) as the
  first lesson; the stair's landing plate fires a volley from a murder hole over
  the stair; the dart gallery's tripwire fires a volley down the gallery from
  above its far barrel; the strongbox is the trapped chest, and opening it drops
  the cobbled patch of roof in front of it as gravel, once.
- No cast. The pass tells the player what it is by its bell, its plates and its
  levers, and two actionbar lines; nobody explains the traps.
- One class, the Carter, carrying a coat, a sword and bread. The toll booth's
  barrel holds a shield, which is a counterplay to the volleys the player may
  or may not think to use.
- The toll bar as the one barred way, raised by an `interact` on a winch lever,
  so the level ends by walking through the gap.
- Low arrow loops in the road wall beside the dart gallery, so the gallery can
  be watched from the road before it is entered (`DW0388`, which advised that
  the gallery's L-shaped approach hid it).

## Posture note

The level says nothing about how a trap works. The bell plate is the one
statement — the wardens heard every step — and the rest is what the player
sees: a plate on a landing, a string between two hooks, a cobbled patch in a
brick roof, and a lever by every trapped mouth.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level
itself; `design/` and `design.json` do not exist, and no showcase camera is
written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.41.0, mc 1.21.11`, the release binary of the
engine's `fix/tripwire-trap-builds` at
`690f0a34d79a68ab3515ad7d4cf9cf6643d36fde` (`cargo build --release -p
delvec`, exit 0) — an unreleased tree, the one that builds a tripwire trap and
fires every trap kind from its PackTest. Its version string is the released
engine's number, so the version alone does not say which engine built this
level; the revision does. The content repository's `versions.toml` was not
touched.

No shipped library taken: both pieces are this campaign's own, written as
grammar programs under `programs/` at program version `1.10.0` and frozen by
`delvec detail` into `prefabs/the-toll-road-*`. The programs were written as
per-course layouts; the disarm levers are not in the pieces, because the
compiler places a disarm's visible lever itself (and the palette allowlist
refuses a lever block in a piece, `DW0730`).

Languages: English, and zh-CN transcreated as a sidecar by the i18n provider
(`tools/creator/i18n-translate.py`, 15 rows, 15 accepted by its fact check),
with four rows rewritten through `delvec l10n-apply`: the class name had been
rendered as a personal name, and the title was re-chosen.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), in dev
mode: the engine worktree's `campaigns` link pointed at this content
worktree. Init's pin check (I1b) reads `~/.delvewright/env.sh` by a fixed
path, and the machine's shared copy names the released engine in creator
mode; the check was run against an environment file of this run's own under a
separate home directory, and exited 0 there (`delvec --version` agrees with
the pin, dev mode, the engine path and the skill root are this run's).

## Trap census, as built

- 3 traps over 3 trigger kinds: `trap/stair-volley` (pressure plate,
  volley, 3 salvos at 24 ticks), `trap/dart-gallery` (tripwire, volley,
  3 salvos at 40 ticks), `trap/strongbox` (trapped chest, collapse of 3 roof
  cells, once). All harmful, none lethal; all three disarmable.
- 1 `step` trigger, `trigger/toll-bell`, on the booth's plate.
- 3 disarm affordances and 1 trapped-chest hitbox: `DW1013 binding: 4 of 4
  interaction summon(s) placed at a cell and judged (dw_trapdis 3,
  dw_trapfire 1)`.
- 4 loot fills: `container binding: 4 container fill(s) (4 loot, 0
  adopting collect), 4 judged against the assembled world`.
- `DW0917` (a trap's cell holds its trigger block) prints no binding line of
  its own; it was perturbed instead: with the tripwire string removed from the
  pass's program, the build refuses with `DW0917` alone, naming
  `trap/dart-gallery` at `[8208, 64, 8222]` holding `minecraft:air`.
- The volley intervals were raised from the default 10 ticks when `DW0918`
  refused them: the walk out of the stair's zone is 16 ticks and out of the
  gallery's 28, and the interval has to leave a player who sets off at a
  salvo at least a fifth of it.

## Target length

`target_minutes` is 15. The critical path measures 46 blocks of route; the
rest of the level is the four strongrooms, each tried with and without its
lever.

## Machine ladder

On the build whose manifest sha256 is
`1bd9de5e5efd11dda13d5ab898f083de97d487cb38c76d2bdff6a950184682b8` (two builds
byte-identical, 121 files), all run locally (the remote build machine had no
free slot):

- `validate` exit 0; `build` exit 0.
- PackTest: **green**, all 21 required tests passed (20 templates in the
  build's test directory), among them `v06_trap_fire_stair_volley`,
  `v06_trap_fire_dart_gallery`, `v06_trap_fire_strongbox`, `v06_volley`,
  `v06_collapse`, `v06_loot` and `env_trigger_toll_bell`.
- Bot: critical path passed, 4 steps; 3 of 3 owed cues arrived. It walks the
  road, raises the bar and walks through; it enters no strongroom. Die-retry
  and the death loop are unbound (no combat, no death plan), as the run
  states. No branch plan is emitted.
- Written world (`DW0955`): 3536 non-air cells compared, 0 differing in the
  model class; 13 grass cells turned to dirt (random tick).
- Staging gate: not run here; it runs at `playtest-server.sh up`.

## Visual review — deferred

No Chunky scene was rendered; the visual review waits for the Lumenwright
review frames. Two CPU drafts (`delvec snapshot`) were looked at: from above
the foot of the pass, and down the road from the spawn. The pass reads as a
walled road with the strongroom mouths in its walls; the drafts draw no
entity, so the disarm levers (entities the compiler places) and the toll bar
(a gate region the model shows cleared) are not in them.
