# The Tide Mill — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0016 §4 (timed gates) pinned: a
mill race where the water gate cycles; the whole level is timing runs through
three gates, with escalating windows. One mechanic, small, minimum cast.

## What was invented here

- The fiction: the tide mill at Saltmarsh Reach, its miller long gone, its
  wheel still turning on the ebb and still working three paddle gates in the
  dry race below it; the party as porters going up from the sea wall to the
  mill yard.
- "Escalating windows" read as windows that tighten: 80/40, 50/50 and 30/70
  ticks open/shut, which `DW0378`'s arithmetic over the one-block span (two
  moves at four ticks a block) gives as 60%, 43% and 23% of each cycle
  admitting a crossing. The third sits just over the 20% floor on purpose.
- `crush: true` on all three paddles. A timing gate that only delays a
  mistimed body teaches nothing, and `DW0378`'s proof is what makes an
  absolute penalty fair; a checkpoint in each pound past a paddle makes the
  death cost one paddle, not the race.
- The live channel beside the walk, behind a wall two courses high, so the
  race carries its water without the walk ever being water.
- Pounds eight blocks long, so each has ground five or more blocks back from
  the next paddle to stand and watch a cycle from.
- One class, the Porter, with boots and bread. No cast, no dialogue; the
  objective hints carry the one instruction (watch it, then go).

## Posture note

The level states nothing about how a paddle works beyond the objective hints.
The board, its beam and its rhythm are the statement; the player watches one
cycle or pays for not watching.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.41.0, mc 1.21.11`, the release binary of the
engine at `d1d499c71b9227ec68593568bfb2016f209f88d8` (`cargo build --release
-p delvec`, exit 0). Its version string is the released engine's number, so
the version alone does not say which engine built this level; the revision
does. The content repository's `versions.toml` was not touched.

No shipped library taken: both pieces are this campaign's own, written as
grammar programs under `programs/` at program version `1.10.0` and frozen by
`delvec detail` into `prefabs/the-tide-mill-*`. The race declares four spaces
(the four pounds) joined by three barred contract edges whose bars are the
paddles, so the piece's own contract proves that each paddle is the only way
from one pound to the next (`contract-edge-proof`, 3 of 3 interior edges).
The headstock over each paddle stops a course short of the race's top so the
race's length is measured through it (`DW0833` measures a clear run at the top
course of the play space, and a headstock reaching it cut the measure to 8).

Languages: English, and zh-CN transcreated as a sidecar by the i18n provider
(`tools/creator/i18n-translate.py`, 17 rows, 17 accepted by its fact check).

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), in dev
mode: the engine worktree's `campaigns` link pointed at this content worktree.
Init's pin check (I1b) reads `~/.delvewright/env.sh` by a fixed path, and the
machine's shared copy names the released engine in creator mode; the check
was run against an environment file of this run's own under a separate home
directory, and exited 0 there.

## Timed-gate census, as built

- 3 timed gates, all `crush: true`, all phase 0: `timed-gate/first-paddle`
  (80/40), `timed-gate/second-paddle` (50/50), `timed-gate/third-paddle`
  (30/70), each a 3 × 3 × 1 board of spruce planks across the walk.
- `DW1011 binding: 3 gate(s) resolved … 3 clocked, … 0 got round by walking,
  falling, jumping or swimming`.
- Each of the first three critical-path legs carries exactly one gate in
  `validation/critical-path-waypoints.json` (3 of 3 gates crossed on the
  route); the fourth leg, into the yard, carries none.
- `DW0378` and `DW0388` print no binding line of their own. `DW0378` was
  perturbed instead, once per gate (below). `DW0388` (observability; warning
  tier here, as the campaign declares no bonfire) raised nothing and was not
  perturbed.

## Target length

`target_minutes` is 12. The critical path measures 42 blocks of route by the
graph's projection (22 measured over the built blockout's one projected leg);
the rest of the level is waiting at, watching and retrying three paddles.

## Machine ladder

On the build whose manifest sha256 is
`f264643decd30e59b139d45793594f133c1fc584a89ccb2ffd6dd2e1d05c7d19` (two local
builds byte-identical, 121 files; the remote build machine's build of the same
two revisions gave the same manifest hash):

- `validate` exit 0; `build` exit 0.
- PackTest (local): **green**, all 21 required tests passed (20 templates in
  the build's test directory), among them `souls_timed_gate_*` (one per gate:
  re-seal, open, close) and `souls_timed_gate_crush_*` (one per gate: the
  closing selector holds a body standing in the gate and releases one two
  blocks clear), and `v06_checkpoint_respawn`.
- Bot (remote): critical path passed, 6 steps; 5 of 5 owed cues arrived. At
  each paddle it staged at the edge, waited for the paddle to shut and open,
  and crossed in the window. Die-retry is unbound (no combat), and the death
  loop is unbound: the harness counts no death plan in a campaign with no
  lethal volume, `on_death` or stake, so a crush death and the checkpoint
  respawn after it are not walked by the ladder.
- Written world (`DW0955`, remote): 1271 non-air cells compared, 0 differing
  in the model class; 4 grass cells turned to dirt (random tick); 9 cells of
  the first paddle written shut and saved open (the clock class).
- Staging gate (local, run against this build and the two records):
  **refused** on one row, `bell-08` UNBOUND: its population is this
  campaign's 3 checkpoints, its binding is `respawn-safety.json`'s pair count,
  and with no hostile force in the campaign the pair count is 0 — which the
  artifact itself says is the honest answer. Recorded as a toolchain finding;
  the campaign was not changed to dodge it.

## Perturbation

In a scratch copy, each gate in turn set to 20 ticks open and 80 shut: the
build refuses with `DW0378` alone, naming that gate — "crossing its span takes
8 ticks (2 blocks at 4 t/block), so only 13 of its 100-tick cycle (13%) admit
a player who starts walking then", exit 3. All three gates refused by name.

## Visual review — deferred

No Chunky scene was rendered; the visual review waits for the Lumenwright
review frames. Two CPU drafts (`delvec snapshot`) were looked at: from above
the sea-wall end looking up the race, and at eye height in the tail pound.
The race reads as a walled channel with the water beside the walk and three
dark headstocks across it; the drafts draw the paddles open (the model's
clocked regions are cleared).
