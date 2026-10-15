# The Bell Changes the Tune

> **Requires delve engine 0.47.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

Hollin Chapel stands in a walled churchyard, and its passing bell has not been
rung in forty years. The vigil book asks for it once at dusk, for the names on
the stones. Walk up through the yard, ring the bell at the altar, and listen to
what the yard does with the sound.

One player, about ten minutes. You arrive as a **Ringer**, with a lantern for
the path and a heel of bread for the vigil.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
server's resource pack: it carries the Chinese text. Set the client to 简体中文
to play it in Chinese.

This level is for listening, so have the music loud enough to hear before you
start.

**The yard's first track is spaced, as the game's own background music is.**
It waits between two and five minutes between plays. Step into the chapel and
back out before you ring the bell, and the yard may be silent for a while: that
silence is the wait the yard declares, not a fault.

## What this level is for

It is the demo level for **a scene states its music**. Every place in the
level, and the ground under it, says what it plays — a track, or silence — and
the story changes the music by changing the place. Nothing here can be
confirmed by a machine: the game decides music on your client, so the fade, the
loop and the toast are yours to hear.

## What to listen for

1. **The yard's track starts, then fades as you step into the chapel.** A soft
   piece from the meadow set begins a few seconds after you join, standing at
   the lychgate. Walk up the path and in at the door. Does the music fade away
   once you are under the roof, rather than stopping dead? Roughly how long does
   the fade take? (The game's own curve is about fifteen seconds; time it from
   the doorway.)
2. **What the now-playing toast shows.** If your client shows the now-playing
   toast, it names the piece and its artist in the corner of the screen when
   the yard's track starts, and again when the bell's tune starts. Is it the
   piece you hear?
3. **The cut when you walk back out.** Ring the bell at the altar, then go back
   out of the door. The yard now plays a different, harsher piece. Does it come
   in at once as you cross the threshold — cutting off anything still fading,
   rather than waiting its turn? Ring quickly (within fifteen seconds of
   entering) and the yard's first track will still be fading when you leave:
   does the new one cut it?
4. **The loop's seam.** Stay out in the yard for two minutes. The new piece is
   short and plays back to back, with no gap. Can you hear where it ends and
   starts again?
5. **The dread stops at the chapel door.** Walk back in. Does the harsh piece
   stop dead as you step inside, instead of fading out over fifteen seconds the
   way the first track did?
6. **The last look over the yard has its own music.** The level ends with a
   camera looking down over the yard toward the chapel, and the shot is scored
   with a slow lament of its own. Does the lament come in at once with the
   shot, rather than after a pause? When the shot ends you are back where you
   stood, inside the chapel: does the lament fade there, as the yard's first
   track did? Step back out into the yard: does the harsh piece take it back at
   once?

## The refusal

A place that does not say what it plays is refused before anything is built.
`transcripts/a-chapel-that-leaves-the-music-to-the-game.txt` is the shipped
campaign with one line removed — the chapel's `audio/background_music` — run
through `delvec validate`:

```
DW1031 [error] world /content/atmospheres/1/attributes: atmosphere `atmosphere/chapel` does not state its music: its `attributes` carry no `audio/background_music`. A biome that declares none inherits the overworld dimension's, vanilla's calm overworld music, so a camera standing in this place would hear a track nobody chose. Add `audio/background_music`: `{}` for silence, or `{"default": {"sound": <id>, "min_delay": <ticks>, "max_delay": <ticks>, "replace_current_music": <bool>}}` for a track.
```

## Hosting it

Add `-e DELVE_RESET_WHEN_EMPTY=90` and the world is thrown away and built again
from the image once nobody has been online for 90 seconds, so the next arrival
starts a delve nobody has touched — but then EVERY start resets, and restarting the
container under a party ends that party's run. Leave it out and the world is kept.
The floor is 60 seconds; below it the server refuses to start.
