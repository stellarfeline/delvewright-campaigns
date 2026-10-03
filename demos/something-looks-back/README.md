# Something Looks Back

The demo level for **a perception bundle** (spec-0085): a `sequence` of
`give-effect`, `particle` and `play-sound` played to an audience — the
envelope's `audience` and `in`, a timeline that keeps its actor, the
full-screen `particle`, a sound in the listener's own frame — and the
blind-reach refusal that keeps a blinding away from a hazard.

The level is a campaign, so it lives where every campaign lives:

    campaigns/something-looks-back/

## What it is

A walled court at noon with three alcoves off it, each holding one heavy
pressure plate you press (right-click), and an archway north to a lava pool
behind a fence rail.

- **The court** (x 8208–8239, z 8212–8243, floor at y 64). You arrive at its
  centre (8223, 64, 8227).
- **The west plate** (8202, 64, 8227) plays the beat **to whoever pressed it**
  (`"audience": "actor"` on every step). A second player standing beside the
  presser sees and hears nothing but the court.
- **The east plate** (8244, 64, 8227) plays it **to everyone standing in the
  court** (`"in"` the court's box). A player in an alcove sees nothing — the
  presser included, since the plate is in its alcove.
- **The south plate** (8223, 64, 8248) plays it **to everyone**.
- **The pit** (centre about 8223, 64, 8204) is a three-by-three pool of lava let
  into the floor, a one-cell ledge round it, and a dark-oak fence rail round the
  ledge. The rail is a wall a body cannot cross, so the ledge — the only floor a
  body could step into the lava from — is floor nobody can walk to. That is what
  lets the south plate blind everyone: no player can be standing where a blind
  step kills.

The beat, each plate's: at tick 0 **darkness** 8 s and **nausea** 10 s (both
`hide_particles`), the full-screen **elder guardian face**, and two sounds; at
tick 50 **blindness** 2 s, a second face and a second sound; at tick 110 a
**warden's breath three blocks behind you** (`"at": {"at": "players",
"offset": [0, 0, -3]}`). Pressing the plates is the critical path (west, east,
south, then back to the middle of the court).

## What to look for

Serve it locally (below) with **two players** if you can. Walk it twice: once
at full settings, once at **Distortion Effects 0, Darkness Pulsing 0, Particles
Minimal** (Options → Accessibility and Video Settings). The round summary
records what survived the second pass, per effect.

1. **At the spawn**, an ordinary noon court. Look north through the arch: the
   lava glows behind its rail.
2. **Press the west plate.** The screen darkens and swims; the elder
   guardian's face fills it; a curse and a heartbeat. The second player, beside
   you, sees and hears nothing. About 2.5 s in, a blind cut with a second face.
   About 5.5 s in, a breath **behind you** — turn round: it should come from
   three blocks behind, at ear height, wherever you were looking.
3. **Press the east plate** with the second player standing in the court: they
   get the beat, you (in the alcove) do not.
4. **Press the south plate**: both of you get it, wherever you stand.
5. **The particles at Minimal**: on the second pass, does the face still draw?
   Every particle is written in force mode, which the wiki says is drawn at
   every setting; this is where that is confirmed for the face.
6. **Darkness Pulsing 0 / Distortion Effects 0**: the darkness should stop
   pulsing but keep its fog; the nausea warp should be gone (a green vignette
   at most). The beat is never the only signal — here it carries no message at
   all.
7. **Re-press a plate inside its own length** (the beat lasts about 10 s): a
   second grant of an effect you already have shows nothing unless it is
   stronger or longer, so expect less the second time; and the timeline
   re-times for every player it carries.
8. **Walk back to the middle of the court.** The delve ends.

What this level does not show, stated: a fall that hurts and does not kill, a
player already blind from a potion of their own, and momentum a sprint carries
into a blinding — none of them is in the engine's model, and none is here.

## What the engine refuses (the fourth declaration)

The same campaign with one edit — the south plate's blindness step drawn `in`
a box over the ledge inside the rail (`{"anchor": "anchor/node-pit",
"extent": [2, 0, 2]}`) — built with the same engine. The transcript,
verbatim:

```
DW0943 [error] build: after world-edits batch `batch/the-pit`: blinding grant `minecraft:blindness` for 2 s at quests /content/quests/0/on_objective_complete/obj/press-plate-three/0/steps/1/effects/0 hides the floor from players standing in 16 cell(s); in 9 move(s) — walking, since it forbids the sprint — a body reaches 16 cell(s), and 12 of them can be caught: y=64 (12 cell(s): [8221, 64, 8203], [8221, 64, 8204], [8221, 64, 8205], [8222, 64, 8202], [8222, 64, 8206], [8223, 64, 8202], and 6 more on the same floor). First: beside [8221, 64, 8203] a body steps into lava at [8222, 64, 8203]. Danger is visible, or the engine refuses it, and a blinded player cannot see the hazard beside them. Shorten `seconds` so the reach stops short; draw `in` so the standing set is farther from the hazard; use `minecraft:nausea`, which leaves the floor visible; or move the volume as DW0891's remedy says. Never remove a cell from the walk.
```

## Serve it locally

From the engine repository at the branch that carries the perception bundle
(`feat/perception`), with this content repository's worktree as the library:

```
tools/creator/playtest-server.sh up <content>/campaigns/something-looks-back --prefabs <content>/prefabs
```

then Multiplayer → Direct Connect `localhost:25565`, pick **Walker**, and walk
the steps above. `tools/creator/playtest-server.sh down` when done. The level
is never copied into a singleplayer save.

The staging gate refuses this build: 6 of 122 findings have no live, binding
check on it — `isl-02` and `isl-41` (no interaction carries `requires_item`),
`isl-35` and `isl-46` (no cast is declared over its one quest), `drill3-01` and
`drill3-03` (it carries no design record) — objects a demo level does not
author. Serving it takes the gate's own deliberate override
(`--stage-anyway "<reason>" --acknowledge-red 6`).

## State

Built and machine-proven with the engine at `feat/perception`: PackTest 18 of
18 required tests; the critical-path bot passes (it presses all three plates
and walks back); `blind-reach binding: 6 blinding grant(s) examined; standing
sets of 1319, 1319, 1319, 1319, 961 and 961 cell(s); reaches of 45, 9, 45, 9,
45 and 9 move(s); 0 caught.` Not yet walked by a person, so every client-side
question above is open.
