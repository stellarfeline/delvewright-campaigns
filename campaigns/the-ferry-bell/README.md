# The Ferry Bell

> **Requires delve engine 0.42.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

![The shore, the jetty and the ferry house from the south-east](media/panorama.jpg)

A wet afternoon on a sandy shore. The ferry lies over on the far side of the
sound, and it only crosses when its bell is rung. The bell is in the ferry house
at the end of the jetty, bolted in. Nell Garrow has kept it for thirty years,
and she will not ring it alone: the last three times it rang, the dead came up
out of the cove onto the spit across the water.

One player, about ten minutes. You arrive as a **Traveller** with a boathook, an
oilskin and a heel of bread.

**Nell Garrow**, the ferry-keeper, waits in the rain at the jetty mouth with one
arm tucked into her coat.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
server's resource pack: it carries Nell's face and the Chinese text. Set the
client to 简体中文 to play it in Chinese.

![The view from where you arrive](media/arrival.jpg)

## What this level is for

It is the demo level for **guidance a player can follow**: a player who has
never pressed a key in Minecraft can tell, at every point, what to do next and
which key does it, and nothing in the level glows, floats or points. Every step
is either in plain sight of where the last one left you, or it is told in a hint
when it begins. Every step's title starts with the verb of what your hands will
do, in English and in Chinese. The first time a kind of action is needed, Nell
tells you which key does it — your own key, as your client has it bound.

## What to look for

Play it once in English and once in 简体中文. No step shows a marker.

1. **The opening teaches right-click before the first click is owed.** As the
   delve starts, the first objective appears (*Talk to the ferry-keeper* /
   *与渡船看守交谈*) and Nell's line follows it in chat: *If you want a word
   with anyone on this shore, stand close and press …*. Does the key in that
   line read as **your** binding (by default *Right Button*; rebind *Use Item*
   and it changes)? Does the line arrive before you have had to click anything?
2. **The second teaching line comes with the notice.** When *Read the ferry
   notice* appears, a second line says signs, levers and bells answer to the
   same key. Does a player who has only ever clicked a person now know to click
   the sign?
3. **Each next step reads from where you stand.** From Nell, can you see the
   notice on its post east of the jetty mouth? From the notice, can you see the
   lever on the deck beside the ferry-house door, sixteen blocks out along the
   jetty? Only one step carries a hint — the bell, which stands inside the
   house where the door hides it (*Inside the ferry house, on its stand in the
   middle of the floor*). Is anything you are asked to do somewhere you could
   not find without a marker?
4. **The lever reads as the one thing to pull.** It is a lever on the deck
   floor, one block in from the rail's last post, beside the bolted door. Does
   it read as the bolt's lever, and as the only thing there to pull? (Its first
   build put it on the rail, among the rail's posts; see *The refusals*.)
5. **The fight across the water reads as forming up before it reaches you.**
   Ring the bell. Three of the dead come up on the spit across the cove, in
   view through the slit window in the house's east wall, about fifteen blocks
   away. A third teaching line names the attack key. Do they read as gathering
   over there, and then coming for you round the shore, rather than appearing
   beside you?
6. **The place.** Does the shore read as a ferry landing in the rain — a beach,
   a railed jetty, a small timber ferry house at its end on the water, a fenced
   spit across the cove where nets are dried?

If you die in the fight you come back on the jetty, with the dead still
standing where they were.

## The refusals

The level was first built with the bolt lever on the jetty rail, among the
rail's spruce fence posts. Each run below is the full campaign with the edit
named, through `delvec build`; the transcripts in `transcripts/` are verbatim.

**The lever among the rail's posts** (`transcripts/lever-on-the-rail.txt`,
exit 3). The rail hides it: from the notice, the line of sight to the lever
meets the next post first.

```
DW0863 binding: 5 act(s) over 1 walk(s) — 1 announced with a hint, 3 in sight (1 kill(s) also in reach), 0 trigger(s) judged by sight alone; 1 refused; 0 kill(s) on no walk judged from the acts that fire their wave
DW0863 [error] build: on the critical path, the `interact` act `obj/draw-the-bolt` cannot be found by the party: from `obj/read-the-notice`'s cell ([8214, 64, 8209]) its target [8208, 64, 8198] is 12.6 blocks away and hidden: the line is stopped first at [8208, 64, 8199]. An act the party can see from where it stands needs no line; one it cannot see owes one. It is not announced with a hint (it has no `hint`). Give `obj/draw-the-bolt` a `title` and a `hint` that says where it is, or move the act or its target into sight of where the party stands.
```

**The same, with a hint** (`transcripts/lever-on-the-rail-with-a-hint.txt`,
exit 0). Given the hint *On the jetty's west rail, a few steps out from the
shore.*, the build reaches the twin check and passes it: a lever is not a
fence, so a lever among fence posts is not among its own kind.

```
DW1017 binding: 3 pressable(s) — 3 alone within 3.0 blocks, 0 marked; 0 refused among 0 twin cell(s)
```

**A pole lever among its posts** (`transcripts/a-pole-lever-among-its-posts.txt`,
exit 3). The same hinted build with the lever's prop made of the rail's own
block — a spruce fence pole to pull:

```
DW1017 binding: 3 pressable(s) — 2 alone within 3.0 blocks, 0 marked; 1 refused among 6 twin cell(s)
DW1017 [error] build: `interact` objective `obj/draw-the-bolt` is pressed at [8208, 64, 8198] on a `spruce_fence`, and 6 more `spruce_fence` stand within the click's reach (3.0 blocks) of it: [8208, 64, 8195] at 3.0 blocks, [8208, 64, 8196] at 2.0 blocks, [8208, 64, 8197] at 1.0 blocks, [8208, 64, 8199] at 1.0 blocks, [8208, 64, 8200] at 2.0 blocks, [8208, 64, 8201] at 3.0 blocks. Nothing tells the party which one to press. Move the twins away, change the prop to a block the scene has one of, or mark the act (a prop-less `interact` with `marker: shown`). Do NOT move the anchor into a wall to satisfy this: the cell a body presses is the cell this reads.
```

The lever was then moved off the rail to the deck beside the door, where the
notice sees it, and the level builds.

## The machine record

The build that ships (`delvec build`, exit 0, twice, byte-identical: 172
files):

```
DW0863 binding: 5 act(s) over 1 walk(s) — 1 announced with a hint, 4 in sight (1 kill(s) also in reach), 0 trigger(s) judged by sight alone; 0 refused; 0 kill(s) on no walk judged from the acts that fire their wave
DW1015 binding: 10 title(s) and 2 hint(s) over 2 language(s) judged (0 string(s) in languages with no table); 0 refused
DW1016 binding: 3 class(es) required over 1 walk(s) — 3 taught by a line, 0 declared taught by the level; 0 refused
DW1017 binding: 3 pressable(s) — 3 alone within 3.0 blocks, 0 marked; 0 refused among 0 twin cell(s)
name-told binding (DW0982): 4 declared name(s); 1 walk(s); 10 of 10 dialogue string(s) and 6 of 6 objective string(s) on screen on some walk; 0 use(s) of a name in them, 0 untold
```

- PackTest: all 37 required tests passed. Two of them drive a teaching line
  (talking to Nell, and the fight); the notice's line is emitted but no test
  asserts it.
- Bot critical path: passed in 7 steps, with 2 scripted deaths in the fight
  survived; the wave's three bodies were read against the document (3 facts, 3
  matched); Nell's turn to face the player was asserted 13 times.
- The world the server wrote equals the engine's model at every compared cell
  (17894), outside 6 fence-end states the server re-derives.
- Staging gate: refused with 2 of 127 findings unbound, both for the design
  record a demo level does not carry (`drill3-01`, `drill3-03`); 39 bound, 26
  declared uncoverable, 60 inapplicable. Serving it takes the gate's own
  override.

## What this level does not show

- **The notice is blank.** A sign prop carries no text; its words arrive in
  chat when you click it.
- **Rain.** The renders above are drawn without rain, clouds or rain fog; in
  the game it is raining all through.
- **The dead are zombies** — the dead of this shore, kept from burning in the
  daylight by the rain.
