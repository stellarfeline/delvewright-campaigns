# Something Looks Back

The demo level for **a perception bundle** (spec-0085): a `sequence` of
`give-effect`, `particle` and `play-sound` played to an audience — the
envelope's `audience` and `in`, a timeline that keeps its actor, the
full-screen `particle`, a sound in the listener's own frame — and the
blind-reach refusal that keeps a blinding away from a hazard.

The level is a campaign, so it lives where every campaign lives:

    campaigns/something-looks-back/

## What it is

A walled court at noon, open to the sky. Three shallow alcoves are let into
its west, east and south walls, each open to the court along its whole
width, and each with one lever on its floor. A doorway in the north wall
leads to a small room with a lava pool behind a fence rail.

- **The court** (x 8208–8239, z 8212–8243, floor at y 64). You arrive at its
  centre (8223, 64, 8227).
- **The alcoves** are 8 cells wide and 4 deep: west x 8203–8206, z 8224–8231;
  east x 8241–8244, z 8224–8231; south x 8220–8227, z 8245–8248. From the
  court each one reads as a wide recess under the court wall, with open sky
  over it.
- **The levers** are there from the moment you arrive, all three at once.
  You **right-click** a lever to fire it, in any order. The lever does not
  flip when you click it: the click is taken by the invisible hitbox around
  it, and the chat says the objective is complete.
- **The west lever** (8204, 64, 8227) plays the beat **to whoever pulled
  it** (`"audience": "actor"` on every step). A second player standing beside
  the puller sees and hears nothing but the court.
- **The east lever** (8242, 64, 8227) plays it **to everyone standing in the
  court**: `"in"` the court's anchor box, x 8208–8238, y 61–67, z 8212–8242.
  A player in an alcove sees nothing. That includes the puller, since the
  lever is in its alcove.
- **The south lever** (8223, 64, 8246) plays it **to everyone**.
- **The pit room** is north of the court through the doorway. In its middle
  (centre 8223, 64, 8204) is a three-by-three pool of lava let into the floor
  (x 8222–8224, z 8203–8205). A one-cell ledge runs round it, and a dark-oak
  fence rail runs round the ledge (x 8220–8226, z 8201–8207). The rail is a
  wall a body cannot cross. So the ledge, the only floor from which a body
  could step into the lava, is floor nobody can walk to. That is what lets
  the south lever blind everyone: no player can be standing where a blind
  step kills. The lava is flush with the floor and hidden behind the rail, so
  it cannot be seen from the court. Walk through the doorway to see it.

The beat is the same for each lever. At tick 0: **darkness** 8 s and
**nausea** 10 s (both `hide_particles`), the full-screen **elder guardian
face**, and two sounds. At tick 50: **blindness** 2 s, a second face and a
second sound. At tick 110: a **warden's breath three blocks behind you**
(`"at": {"at": "players", "offset": [0, 0, -3]}`). The critical path is the
three levers (the bot takes them west, east, south) and then a walk back to
the middle of the court.

## What to look for

Serve it locally (below) with **two players** if you can. Walk it twice: once
at full settings, once at **Distortion Effects 0, Darkness Pulsing 0, Particles
Minimal** (Options → Accessibility and Video Settings). The round summary
records what survived the second pass, per effect.

1. **At the spawn**, an ordinary noon court. Turn round: three wide recesses
   in the walls, west, east and south, each with a lever on its floor, and a
   doorway north.
2. **Pull the west lever.** The screen darkens and swims. The elder guardian's
   face fills it. You hear a curse and a heartbeat. The second player, beside
   you, sees and hears nothing. About 2.5 s in, a blind cut with a second
   face. About 5.5 s in, a breath **behind you**. Turn round: it should come
   from three blocks behind, at ear height, wherever you were looking.
3. **Pull the east lever** with the second player standing in the court:
   they get the beat, and you, in the alcove, do not.
4. **Pull the south lever**: both of you get it, wherever you stand.
5. **The particles at Minimal**: on the second pass, does the face still draw?
   Every particle is written in force mode, which the wiki says is drawn at
   every setting. This is where that is confirmed for the face.
6. **Darkness Pulsing 0 / Distortion Effects 0**: the darkness should stop
   pulsing but keep its fog, and the nausea warp should be gone (a green
   vignette at most). The beat is never the only signal; here it carries no
   message at all.
7. **Click a lever a second time**: nothing plays. Each lever fires once.
   After that its hitbox is gone, so the click reaches the lever itself: it
   flips, as any lever does, and nothing else happens.
8. **Walk back to the middle of the court** once all three have fired. The
   delve ends.

What this level does not show: a fall that hurts and does not kill, a
player already blind from a potion of their own, and momentum a sprint carries
into a blinding. None of them is in the engine's model, and none is here.

## What the engine refuses (the fourth declaration)

The same campaign with one edit, built with the same engine: the south
lever's blindness step is drawn `in` a box over the ledge inside the rail
(`{"anchor": "anchor/node-pit", "extent": [2, 0, 2]}`). The transcript,
verbatim:

```
DW0943 [error] build: after world-edits batch `batch/the-pit`: blinding grant `minecraft:blindness` for 2 s at quests /content/quests/0/on_objective_complete/obj/pull-lever-three/0/steps/1/effects/0 hides the floor from players standing in 16 cell(s); in 9 move(s) — walking, since it forbids the sprint — a body reaches 16 cell(s), and 12 of them can be caught: y=64 (12 cell(s): [8221, 64, 8203], [8221, 64, 8204], [8221, 64, 8205], [8222, 64, 8202], [8222, 64, 8206], [8223, 64, 8202], and 6 more on the same floor). First: beside [8221, 64, 8203] a body steps into lava at [8222, 64, 8203]. Danger is visible, or the engine refuses it, and a blinded player cannot see the hazard beside them. Shorten `seconds` so the reach stops short; draw `in` so the standing set is farther from the hazard; use `minecraft:nausea`, which leaves the floor visible; or move the volume as DW0891's remedy says. Never remove a cell from the walk.
```

## Serve it locally

From the engine repository at the branch that carries the perception bundle
(`integration/stranding-capabilities`), with this content repository's
worktree as the library:

```
tools/creator/playtest-server.sh up <content>/campaigns/something-looks-back --prefabs <content>/prefabs
```

then Multiplayer → Direct Connect `localhost:25565`, pick **Walker**, and walk
the steps above. `tools/creator/playtest-server.sh down` when done. The level
is never copied into a singleplayer save.

The staging gate refuses this build: 2 of 122 findings have no live, binding
check on it, `drill3-01` and `drill3-03`, because it carries no design record,
which a demo level does not author. Serving it takes the gate's own
deliberate override (`--stage-anyway "<reason>" --acknowledge-red 2`).

## State

Built and machine-proven with the engine at
`integration/stranding-capabilities`. PackTest: 19 of 19 required tests
pass. The critical-path bot passes in 6 steps: it walks to each lever, proves
its crosshair reaches the lever's hitbox, and fires the objective with the
objective's `/trigger` command rather than a mouse click, then walks back.
`blind-reach binding: 6 blinding grant(s) examined; standing sets of 1241,
1241, 1241, 1241, 961 and 961 cell(s); reaches of 45, 9, 45, 9, 45 and 9
move(s); 0 caught.` Not yet walked by a person, so every client-side question
above is open.
