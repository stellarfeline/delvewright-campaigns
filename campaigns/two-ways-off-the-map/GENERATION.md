# Two Ways Off the Map — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0113 (a body can be where the game
lets it): three small scenes under one sky. The yard, a chapel yard ringed by a
wall with standing stones in it, one stone in front of a buttress that a sprint
jump reaches and a second jump clears the wall from, refused by `DW0921` and
repaired by moving the stone one cell. The jetty, a plank jetty over an `ocean`
horizon with a ledge a body jumps off into the sea and no rim within reach,
refused by `DW0322` and repaired by a stair into the water. The course, five
declared jumps on a parkour line, each proven and driven by the bot, and a
sixth of five columns flat declared and refused by the jump proof.

## What was invented here

- The fiction: a chapel on a rock in the sea, the boat that leaves from the end
  of the jetty, and the broken wall-walk over a flooded cistern between them.
- The yard is the Bell yard of the engine's own reach-graph tests rebuilt at
  full size: the inner yard walled three high, the buttress two high against
  its east wall, the stone one high in front of it. Past the east wall is a
  strip of old burying ground walled five high on every side, so a body that
  gets over the wall lands somewhere it cannot leave. The yard's north side is
  the chapel's ruined south wall with two glazed lancets; its south wall is the
  cistern's north wall too and stands six high, a gate through it onto the
  wall-walk. The other four standing stones are one high and stand well away
  from the walls and the buttress.
- The jetty's deck is six courses over the sea (walk plane y 68, the sea's top
  course y 62), railed with spruce fence along both sides and across its head.
  The plank is a block of spruce planks against the north rail halfway out.
  The stair goes down off the south side near the head, from a gap in the rail,
  to a two-cell landing at the water's top course.
- The course: platforms three wide down the middle of a cistern five wide,
  walled to four courses over the grade, its floor three courses below the
  platforms. The leaps, west to east: two, three and four columns on the flat
  (gaps of one, two and three); three columns up one onto the raised fourth
  platform (a gap of two); four columns down one off it (a gap of three), under
  a lid of deepslate tiles laid across the cistern's walls three cells over the
  fourth platform's top. Each platform gives a straight run-up of five or six
  cells. One course of water lies over the cistern's floor, and one stair, at
  the near end by the gate, comes back up out of it onto the first platform: a
  body that falls lands in the water and wades back to that stair, so a fall
  starts the course again. Nothing else leads up out of the water.
- The route: the first objective is the raised fourth platform, which only the
  four leaps before it reach and only the fifth leaves; the second is the head
  of the jetty. No speaking cast, no fight.

## What the engine forced, and what it could not build as first written

- **Every reach check counts the declared jumps.** The platforms past the
  first, and the jetty, are reached only by the leaps, and the stage-5
  battery's place reachability (`DW0837`) admits them with no stair standing in
  for the leaps: "3 place(s) proven reached".
- **A lid one course thick joined the places by no seam.** Its top was a
  standable cell of the course, and from it the cistern walls' tops lead a body
  down onto the jetty's deck and over the yard's walls into the yard: `DW0838`,
  course to jetty and course to yard. The lid is two courses thick, its top at
  the frame's ceiling and out of the place; the leap under it is unchanged.
- **The jetty's stair is as wide as it is built.** The gap in the south rail
  was claimed with the steps, so the stair's way measured two columns at the
  gap and one clear (`DW1057`). The gap is the deck's own claim, and the way is
  the one column of steps.
- **The piece contract has no jump edge.** A piece's `contract-reachability`
  walks the piece's own blocks, and the course's platforms are joined only by
  leaps. The gate passed over the shipped course, "every one of 409 standable
  cell(s) in declared space is reached", the four platforms only a leap reaches
  among them; which move carried the piece's walk across the gaps is not
  established here, so the pass is recorded as read, not relied on.
- **`DW0921` names the way in, not the whole chain.** The yard's refusal names
  the last movement into the burying ground — the fall off the east wall's top
  — and not the two jumps that got the body onto the wall. That is what the
  engine's leave proof reports (`nav::leave`, the pocket's way in); the two
  jumps are in the stone's place, the buttress and the wall.
- **The jetty's refusal lists the rail tops.** From the plank a body steps onto
  the fence tops, walks them and jumps or falls off anywhere along the jetty, so
  `DW0322` names forty-eight places, the first six in cell order printed; every
  one is reached through the plank.
- The site plan's ocean ground needs a `boundary`, and the horizon states its
  music (silence). Every piece declares every side it shows, its top included.

## Engine and language

Built with `delvec 1.15.0, dsl 0.63.0, mc 1.21.11`, the release binary built at
engine revision `7f3e86f4edc3e711db611b9ce3d3335f1a5d54f6` (the reach-graph
feature, `feature/reachable-surfaces`) on the remote build machine. That
revision is unreleased. The pieces were detailed by the same revision's
release binary on macOS, and a re-detail on the remote build machine changes
no byte.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/two-ways-off-the-map-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The refusals

`refusals/` holds each transcript, with the flag that writes its shape. Each
run was `delvec detail --all` exit 3 with that one error and no other.

- **The yard** (`--yard-as-found`: the stone at yard cell (12, 8), four cells in
  front of the buttress with three of grass between) — `DW0921`:

  > DW0921 [error] build: 1 place(s) a body can get into and not out of — the player is soft-locked there: 75 cell(s) around [8214, 68, 8198] (from critical step 0): a body gets in from [8213, 71, 8198] to [8214, 68, 8198] by a fall of 3 block(s), drifting 1, and no walk, fall, jump or swim leads from any of them back to the route. […]

  `DW0921 binding: … 1498439 cell(s) a body can reach … (179282 of them afloat, 44 on a fence or wall top), 75 it cannot leave`. Repair: the stone moved one cell back, to (12, 7). Probed on the way (stone at each cell, `--stone=X,Z`): from (12, 8), (12, 9), (10, 10), (9, 9), (10, 8), (9, 10) and (8, 10) the buttress is reached and the yard refused; from (12, 7) and (8, 8) it is not.
- **The jetty** (`--jetty-as-found`: no stair into the water) — `DW0322`:

  > DW0322 [error] build: boundary safety (spec-0017, an `ocean` base): 48 place(s) a body can reach let it into 1497866 water cell(s) with NO way back ashore — […]
  > - [8261, 69, 8215] → the open sea at [8258, 61, 8208], by a sprint jump north down 8 into water
  > […]

  Repair: the stair into the water off the south side near the head.
- **The sixth jump** (`build_documents.py --sixth`, `build_pieces.py --sixth`: the
  last platform broken by a gap of four, `jump/five-flat` declared across it)
  — `DW1041`:

  > DW1041 [error] build: declared jump `jump/five-flat` from [8251, 68, 8217] to [8256, 68, 8217] is not makeable: under the game's rules, facing -95° with the jump pressed on tick 25 of the run, the body ended at [8255.70, 65.00, 8216.48]; no run-up up to 6 cell(s) makes it from this launch (the course gives 6) — shorten the gap, lower the landing or raise the launch. […]

  `jumps binding: 6 declared, 5 proven, 1 refused, 0 not a jump; run-ups measured 5..6`. Removed from the shipped level: the declaration and the gap.

## Verification (engine `7f3e86f4edc3e711db611b9ce3d3335f1a5d54f6`, `delvec 1.15.0, dsl 0.63.0`, the release binary sha256 `83c59a3eaa103e2ae410ce0b5c91bfa82c737425c48e5dee137b098f74e414bb`)

The ladder ran on the remote build machine over content `f85a2270ef0584376b493f6c84069660843ffef8`; this record and the storybook, which nothing a build reads, were added after it.

- `build`: exit 0 twice, byte-identical (139 files); `manifest.json` sha256
  `5325e74e982fc4088214c7a9de11fe6b6f70ead3a6069adce5e5f7bef4aa916c`.
- `jumps binding: 5 declared, 5 proven, 0 refused, 0 not a jump; run-ups measured 5..6`
- `reach binding: 1 configuration(s); 1498347 rest state(s) (495 standing, 179508 afloat, 1318344 submerged, 0 holding); 8613886 edge(s) (2174 walk, 1678 fall, 6783 jump, 8591570 dive, 289 climb, 11392 exit); 3108097 launch state(s) simulated, 3132 template arc(s) credited; 3111229 of budget 200000000; survivable fall 22 blocks (unbounded: no)`
- `DW0921 binding: 1 quest configuration(s), 83 route cell(s), 1498347 cell(s) a body can reach by walking, falling, jumping, swimming or climbing (179508 of them afloat, 44 on a fence or wall top), 0 it cannot leave`
- `clear width (DW1057): 4 way(s) […]; 4 way(s) whole, 0 narrowed`
- Blockout battery: 3 places proven reached; `0 place pair(s) joined through the commons (DW0838)`.
- PackTest (`validation/packtest-run.sh`): 17 of 17 required tests passed.
- Critical-path bot (`validation/bot-run.sh`): PASSED;
  `[jump] anchor anchor/high-platform: 4 jump(s) on the proven leg, 4 driven as a parkour hop` and
  `[jump] anchor anchor/jetty-head: 1 jump(s) on the proven leg, 1 driven as a parkour hop`.
- The fall, driven by a harness bot on the same build: set on the raised
  platform at [8238.5, 69, 8217.5], it walked off the south edge, landed in
  the water at [8238.50, 65.00, 8220.60] with health 20, waded west and up the
  near stair, and stood on the first platform at [8205.40, 68.00, 8217.43]
  (the server's own position agreeing), no death, health 20.
- Written world (`validation/world-save.sh`, `delvec written-world`,
  `tools/ci/check-written-world.py`): 0 differing cells of 24131 in every class.
- Staging gate (`tools/creator/staging-gate.py`): stageable with no override,
  all 155 findings carrying a live, binding check or a justified exemption, 98
  of them inapplicable; `validation/staging-admission.sh` admits the tree.

## The design gate

A test level (`world.test_level`) carries no design record: its approved
design is the engine's demo-queue row.
`design/` holds only the scripts; no reference image was drawn.
