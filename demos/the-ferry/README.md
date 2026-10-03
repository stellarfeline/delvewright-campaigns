# The Ferry

The demo level for **a teleport the route proof takes as a link** (spec-0083):
a `teleport` hosted in a `triggers[]` entry declared `once: false`, which the
compiler takes where a walk fails, splices into the critical path as a
`trigger` step with `stand` and `transport`, and counts on the
`DW0311 binding:` line.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-ferry/

## What it is

Two boathouses face each other across a strait. Nothing joins them: no door,
no gap, no bridge. Each has a ferry moored at its jetty — a hull you step down
into, and a tiller beside the hull.

- **The near boathouse** (box x 8200–8211, z 8200–8211, floor at y 64) is
  where you arrive.
- **The far boathouse** (box x 8240–8251, z 8200–8211) is across the strait,
  twenty-eight blocks east.
- **The near ferry**: board it (`obj/board`), which tells the tiller you are
  aboard (`flag/boarded`), then pull the tiller from inside the hull. A short
  cutscene plays the crossing, and when the camera returns you are standing
  in the far boathouse.
- **The far ferry** is the way back, and it only answers once the far shore has
  been reached (`flag/far-shore`), so the return exists when the story asks for
  it.

What you see: the world is the sea (`horizon: ocean`), and each boathouse
stands at the edge of its own shore, a turf bank ringed with sand, with the
strait between them and open water to the north. A boathouse is timber on a
stone footing under a dark-oak gable roof. Inside, an oak jetty runs round a
slip of sea water; the ferry is built of blocks, a dark-oak hull three wide
with a spruce rail, moored bow to a barred water-gate in the north wall and
stern to the jetty. The hull cell is the stern well, and the tiller is the
floor lever just astern of it on the jetty. Windows look across the strait at
the other house, and lanterns hang from the ceiling beams. Every block comes
from `world-edits.json`. The footing runs down to the sea floor and the
water-gate is barred, so nobody swims out of a boathouse. Each side channel of
the slip has a plank step at its stern end, so a body that falls in wades out
onto the jetty.

A player left on the jetty when the tiller is pulled is not carried — the
ferry moves whoever is in its hull. That player boards and pulls the tiller
again, and follows: the trigger is repeatable, which is what makes it a link
rather than a one-shot.

## What to look for

1. **At the spawn** (8205, 64, 8205), the near boathouse: the hull is the cell
   north-west of you (8204, 64, 8204), and the tiller stands beside it
   (8204, 64, 8205). Boarding completes as soon as you are in the hull's
   reach, which the spawn already is.
2. **Pull the tiller from the jetty, outside the hull.** The cutscene plays,
   and you are still on the jetty: the ferry carries only who is in the hull.
3. **Step into the hull and pull the tiller.** The cutscene plays; when the
   camera returns you stand in the far boathouse. The crossing waits for the
   camera: the teleport fires one tick after the cutscene ends.
4. **With a second player**, leave them on the jetty, cross, and have them
   board and pull the tiller: they follow you across.
5. **The far tiller** before you reach the far jetty's middle does nothing; once
   you have (the objective completes), board the far hull and pull it. You are
   carried home.

## What the compile says

The build prints, among its binding lines:

    DW0311 binding: … carried by a link; 2 link(s) declared, … taken; 0 gather(s) declared

and `validation/teleport-gate.json` reads `links: 2, gathers: 0`. The layout
graph draws the strait as two one-way `carry` edges and nothing else.

## The refusals

Each is the campaign with one edit, and each is refused by name:

- **The near tiller's teleport hosted on the boarding objective's completion
  instead** — a teleport fired by an objective is a gather: the first body
  through travels and the jetty player is stranded. The strait's `carry` edge
  then has no link to realise it, and validation refuses it: `DW0934`. (Where
  no graph claims the carry, the walk proof refuses the leg itself, `DW0311`,
  naming the teleport and prescribing a repeatable trigger.)
- **The near lever moved out of reach of its own hull** — to the far
  boathouse's jetty: no cell inside the hull reaches it, so whoever pulls it is
  not carried: `DW0932`, "no stand cell".
- **The teleport fired at the first tick of its own cutscene** — the cutscene's
  end puts everyone back where it started, so the crossing is undone when the
  camera returns: `DW0933`, naming the tick the cutscene ends at and the first
  tick that holds.

## State

Builds on the engine branch `feat/teleport-link`. The machine ladder on the
`validation/` image is green: PackTest runs the generated suite (20 required
tests, among them both links' `env_trigger_*` and `teleport_*` templates), and
the mineflayer critical path boards each hull, pulls each tiller from its
stand cell and is carried both ways (8 steps). With the staging-gate ledger
that reads a demo by its own objects, the gate refuses it on two findings,
both the design record it does not yet carry (drill3-01, drill3-03); it is not
overridden.

Serve it with the engine's playtest server
(`tools/creator/playtest-server.sh up campaigns/the-ferry`), never copied into
a singleplayer save.
