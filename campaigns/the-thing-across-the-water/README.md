# The Thing Across the Water

> **Requires delve engine 0.56.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

You came down the coast road at dusk to a grey bay: a stone jetty running out into the water, a harbour hall at its foot with its wide door standing open, and, out in the bay, a sea-stack of bare rock that nobody looks at for long.

The keeper of the hall, Oswin Marrable, has kept the bell at the end of the
jetty for thirty winters. He has never rung it.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~10 minutes |
| **Mode** | adventure, no combat |
| **Languages** | English, 简体中文 (`zh-cn`) |
| **Class** | one — Traveller, with a lantern |
| **Licence** | CC BY-SA 4.0 |

![The jetty and the harbour hall at dusk](media/jetty.jpg)

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`.

Accept the resource-pack prompt when you join: it carries the delve's Chinese
text.

## For the owner: what to look for

This level is the demo for **a cutscene shot that shows what it is meant to
show**. Walk it once with the client as it comes; each line is one thing to
look at.

1. **Does the keeper show through the open door?** Walk to the hall's door. The
   first cutscene stands on the jetty outside the door and looks straight in:
   the keeper behind his desk at the back of the hall, framed by the doorway,
   for four seconds. Look for him the whole time, not a wall or an empty room.
2. **Does the landscape shot read as the bay?** Speak to the keeper, then walk
   to the bell at the end of the jetty. The second cutscene glides out over the
   water from above the jetty's end for six seconds — a shot of the place, about
   no one thing — then cuts to a slow pass near the sea-stack, aimed at its top.
   Look for: the first half reading as the bay (water, horizon, the stack out
   ahead), and the second half holding the stack in frame.
3. **Does the figure on the sea-stack show the whole time it rises?** Ring the
   bell. The third cutscene stands on the jetty behind the bell and looks across
   ninety blocks of water at the stack for ten seconds while the thing rises out
   of its top, about nine seconds from start to standing. Look for: the figure
   there from the first frame it clears the rock to the last frame of the shot,
   never popping out or flickering, and whether it reads at ninety blocks. The
   build sizes the figure for a client at the lowest Entity Distance the game
   allows (50%): it is drawn out to about 124 blocks there, and the camera is
   never more than 96.4 blocks from it in this shot (the build's
   `validation/shot-subjects.json`: `view_range` 3.87, `farthest` 96.376).
4. **Does any shot frame empty sea, sky or a wall?** Across all three cutscenes.
5. **After the cutscene, is it still there?** Walk back up the jetty and look
   out across the water at the stack: the thing should still be standing on it. Then tell the
   keeper.

On arrival one chat line says the hall's barrels stand empty: the engine owes
that line wherever a container holds nothing, and it is not what this level is
for.

Beside the walk, the five shots the engine refuses — each the level as it ships
plus one edit, printed whole by the same `delvec` in [`refusals/`](refusals/):

| the edit | what the engine says |
|---|---|
| the stack shot aimed twenty blocks up, at sea and sky — [`a-shot-of-sea-and-sky.txt`](refusals/a-shot-of-sea-and-sky.txt) | `DW1033`: the stack is out of frame at tick 0 |
| the keeper shot taken from beside the door, through the hall's wall — [`a-shot-through-the-hall-wall.txt`](refusals/a-shot-through-the-hall-wall.txt) | `DW1033`: all nine sight lines blocked, first by the wall at [8222, 65, 8320] |
| the figure spawned after its cutscene instead of before — [`a-thing-not-yet-standing.txt`](refusals/a-thing-not-yet-standing.txt) | `DW1034`: no beat places it before the cutscene |
| the bell's camera backed off to two hundred blocks, under a view distance of 20 chunks — [`a-figure-two-hundred-blocks-off.txt`](refusals/a-figure-two-hundred-blocks-off.txt) | `DW1034`: 202 blocks against a tracking range of 160 |
| the keeper shot with its subject deleted — [`a-shot-that-names-nothing.txt`](refusals/a-shot-that-names-nothing.txt) | `DW0199`: the shot declares no subject |
