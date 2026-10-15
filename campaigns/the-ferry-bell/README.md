# The Ferry Bell

> **Requires delve engine 0.42.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

![The shore, the jetty and the ferry house from the south-east](media/panorama.jpg)

A wet afternoon on a sandy shore. The ferry lies over on the far side of the
sound, and it only crosses when its bell is rung. The bell is in the ferry house
at the end of the jetty, bolted in. Nell Garrow has kept it for thirty years,
and she will not ring it alone: the last three times it rang, the dead came up
out of the cove onto the spit across the water.

One to four players, about ten minutes. You arrive as a **Traveller** with a
boathook, an oilskin and a heel of bread — and, like everyone, a compass and a
journal.

**Nell Garrow**, the ferry-keeper, waits in the rain at the jetty mouth with one
arm tucked into her coat.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
server's resource pack: it carries Nell's face and the Chinese text. Set the
client to 简体中文 to play it in Chinese.

![The jetty and the ferry house from the shore](media/jetty.jpg)

## What this level is for

It is the demo level for **guidance a player can follow**. Every player carries
a compass that points at one open task, and right-clicking it opens the list of
open tasks to choose from. A lever that does not look like a door's bolt glows
once someone is close to it. And every player holds a journal: how the compass
works, Nell's notes, the open tasks with the one you follow marked, and the
finished ones struck through.

## What to look for

Play it with two players if you can; a few items need a second body.

1. **The compass menu.** Talk to Nell and say you will ring the bell. Two tasks
   open at once: *Read the ferry slate* and *Pull the bolt lever by the
   ferry-house door*. Hold the compass and right-click. Does a list of the open
   tasks appear, with the one you follow marked ◆? Pick the other one. Does the
   needle turn to it, and does chat say *Following: …*?
2. **Two compasses, two ways.** Standing beside Nell, one player follows the
   slate and the other the lever. The slate is a few steps to one side, at the
   jetty's head; the lever is straight out along the jetty. Do the two needles
   point different ways?
3. **The lever glows only up close.** From the shore the lever is a plain lever
   on the deck beside the ferry-house door. Walk out along the jetty. Does it
   start to glow, with a gold outline, only once you are on the last stretch of
   deck, within six blocks of it — and stop when you walk back? Does the glow
   read as *this one*? The bell inside carries no glow: does it still read as
   the bell?
4. **The journal reads in order.** Open the journal (right-click it). Does it
   go: the page about the compass, then two pages of *The Ferry-Keeper's Notes*
   (the first names the use key as your own binding), then one page per open
   task with its hint and the ◆ mark on the one you follow, then the finished
   tasks struck through? Open it again after you pull the lever: has the lever
   moved to the struck-through pages and the bell appeared as open?
5. **Reconnect, or join late.** Disconnect on the jetty and come back, or have
   a second player join after the talk. Does the returning player hold the same
   journal as before, and does the late player hold one that already lists what
   is open and what is done?
6. **Every needle spins at the end.** Ring the bell; three of the dead form up
   on the spit across the water and come round the shore. When the last task is
   done, does every compass needle spin, and is every journal all struck-through
   pages?

If you die in the fight you come back on the jetty, with the dead still
standing where they were.

## How this differs from the guidance row

The row asks for the talk to open the slate and the **bell** together, with the
lever as the way into the house. This engine does not build that: the bell
inside the bolted house has to come after the lever in the quest's own order,
or the route proof refuses the walk into the house. So the talk opens the slate
and the **lever** together, and the bell opens once the bolt is drawn. If you
read the slate after the lever, the compass list holds the slate and the bell,
and you can pick the bell from it.

## The refusal

The level was first built with the bolt lever on the jetty rail, among the
rail's spruce fence posts (`transcripts/lever-on-the-rail.txt`, `delvec build`
exit 3). From the slate, the next post hides it:

```
DW0863 binding: 5 act(s) over 1 walk(s) — 2 announced with a hint, 2 in sight (1 kill(s) also in reach), 0 trigger(s) judged by sight alone; 1 refused; 0 kill(s) on no walk judged from the acts that fire their wave
DW0863 [error] build: on the critical path, the `interact` act `obj/draw-the-bolt` cannot be found by the party: from `obj/read-the-slate`'s cell ([8214, 64, 8209]) its target [8208, 64, 8198] is 12.6 blocks away and hidden: the line is stopped first at [8208, 64, 8199]. An act the party can see from where it stands needs no line; one it cannot see owes one. It is not announced with a hint (it has no `hint`). Give `obj/draw-the-bolt` a `title` and a `hint` that says where it is, or move the act or its target into sight of where the party stands.
```

The lever was then moved off the rail to the deck beside the door, where the
slate sees it, and the level builds.

## The machine record

The build that ships (`delvec build`, exit 0, twice, byte-identical: 211 files):

```
DW0863 binding: 5 act(s) over 1 walk(s) — 2 announced with a hint, 3 in sight (1 kill(s) also in reach), 0 trigger(s) judged by sight alone; 0 refused; 0 kill(s) on no walk judged from the acts that fire their wave
DW1015 binding: 10 title(s) and 4 hint(s) over 2 language(s) judged (0 string(s) in languages with no table); 1 warned
compass binding: 5 tracked objective(s) of 5 — 0 by their own field, 5 by the campaign default; 0 refused
highlight binding: 1 highlight(s) over 5 act(s) — 1 on a block, 0 on a body; 0 refused
journal pages: 16 page(s) measured over the source and every declared language, the fullest 14 of 14 line(s); 0 over
name-told binding (DW0982): 4 declared name(s); 1 walk(s); 10 of 10 dialogue string(s) and 7 of 7 objective string(s) on screen on some walk; 0 use(s) of a name in them, 0 untold
```

- The one `DW1015` warning is the slate's hint, *On its post at the jetty's
  head, right of the planks.*: the lexicon reads *head* as a going verb. Here it
  is a noun, the jetty's landward end, and the hint is kept.
- PackTest: all 41 required tests passed, among them the six guidance tests —
  the compass (aim, the menu's buttons, a pick, the spin, the re-give), the
  compass on a person, the lever's highlight (dark while closed, lit in range,
  dark beyond it), and the journal's pages, a dropped journal, and a joining
  player's journal.
- Bot critical path: passed in 7 steps, with 2 scripted deaths in the fight
  survived; the wave's three bodies were read against the document (3 facts, 3
  matched); Nell's turn to face the player was asserted 13 times.
- The world the server wrote equals the engine's model at every compared cell
  (17894), outside 6 fence-end states the server re-derives.
- Staging gate: refused with 2 of 127 findings unbound, both for the design
  record a demo level does not carry (`drill3-01`, `drill3-03`). Serving it
  takes the gate's own override.

## Review frames

Two draft frames (`delvec snapshot --labels`), with the engine's labels burnt
in. They draw the world as it stands at load, so Nell, the slate's sign, the
lever and the bell are not in them; their labelled boxes are.

- `media/review/at-nell.jpg` — where the talk ends: Nell's box on the left, the
  slate's post (labelled `NOTICE`) on the right, and straight ahead the jetty
  with the lever's box at the ferry-house door: the two open tasks lie in two
  directions.
- `media/review/six-from-lever.jpg` — six blocks short of the lever along the
  deck, the distance at which it starts to glow.

## What this level does not show

- **The slate is blank.** A sign prop carries no text; its words arrive in chat
  when you click it.
- **Rain.** The renders above are drawn without rain, clouds or rain fog; in the
  game it is raining all through.
- **The dead are zombies** — the dead of this shore, kept from burning in the
  daylight by the rain.
- **The glow, in a picture.** No frame here shows the highlight; whether it
  reads is judged in the game.
