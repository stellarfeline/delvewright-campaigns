# The Lamp Across the Water

The demo level for **a campaign declares the view distance its far views need**
(spec-0091): `world.view_distance`, the radius it serves, the refusal of a far
view aimed past it, and the heap the build states for it.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-lamp-across-the-water/

Its two pieces, `prefab/lamp-jetty` (7 × 8 × 21) and `prefab/lamp-tower`
(9 × 30 × 9), are in the prefab library (`prefabs/lamp-jetty.{nbt,json}`,
`prefabs/lamp-tower.{nbt,json}`) and are expanded from the grammar programs in
`campaigns/the-lamp-across-the-water/design/programs/` (seed 1, named in
`zones.json` beside them).

## What it is

Open sea at noon (`horizon: ocean`). A stone-brick jetty with a spruce deck runs
twenty blocks north from where you arrive, to two lantern posts at its end. Two
hundred and fifty-six blocks east of it — the compiler's own stride between
areas — a lighthouse stands on a rock of its own: a stone-brick shaft, a
gallery, a lamp of sea lanterns under a roof, lit at noon.

- **The declaration.** `world.json` says `"view_distance": 20`. The server
  serves 20 chunks, 320 blocks in every direction; the build states the cost in
  `server/resources.properties` (`heap-max=5G`, `players=4`) and in
  `server/README.md`, and the storybook's connect line is followed by the
  render-distance line a player sets.
- **The far view.** When you reach the end of the jetty a six-second shot turns
  east to the lamp, 258.5 blocks from the camera. That shot is what the
  declaration is for, and what the refusal below is about.

## What to look for

1. **At the landing**, look east. With your client's render distance at 20 or
   more, the lighthouse is on the horizon, a thin tower with a lit top. Set it
   to 12 (the client's default) and look again: the sea ends in fog short of it
   and the tower is gone — the server serves the smaller of its number and
   yours, and nothing on the server can raise yours.
2. **Walk out to the lantern posts.** The objective completes at the end of the
   jetty; the cutscene turns to the lamp and the subtitle names it.
3. **Walk back.** The delve completes at the landing.

## The two transcripts

The same campaign, built twice by the same engine (`delvec 1.8.0`, `dsl
0.36.0`):

**With `view_distance` removed** — the engine's floor of 10 chunks, 160 blocks:

```
view distance binding: 10 chunk(s) (the engine's floor, undeclared) serve 160 blocks in every direction; 0 sightline(s) and 0 view(s) judged against it, 0 beyond it.
DW0956 [error] build: cutscene: shot 0 at tick 0 stands at [3.5, 64.5, 19.5] looking at [260.5, 85.5, 1.5], 258.5 blocks away, and the served view distance reaches 160 blocks (10 chunks): what the shot looks at is never sent to the player watching it. Declare `world.view_distance: 17` (the fewest chunks that serve it), or bring the camera path nearer its `look_at`/subject
```

exit 3; no datapack is written.

**As committed, `view_distance: 20`** (17 is the fewest that serve the shot;
20 is the number a player recognises in their own settings):

```
view distance binding: 20 chunk(s) (declared) serve 320 blocks in every direction; 0 sightline(s) and 0 view(s) judged against it, 0 beyond it.
view distance binding: 20 chunk(s) (declared) serve 320 blocks in every direction; 0 showcase camera(s) and 1 cutscene shot(s) judged against it, 0 beyond it; stated to the host: heap-max 5G for 4 players × 1573 chunks each (server/resources.properties).
```

exit 0. `server/server.properties` carries `view-distance=20` and
`simulation-distance=10`; `server/resources.properties` carries `heap-max=5G`.

## The ladder

Built with the engine at the spec's branch; PackTest and the bot critical path
run on the built tree (`validation/packtest-run.sh --project dw-lamp`,
`validation/bot-run.sh --project dw-lamp`): PackTest `All 14 required tests
passed`, the server booted at the build's own ceiling (`[init] Java heap:
MAX_MEMORY=5G (the build states heap-max=5G)`); the bot's critical path
`PASSED (4 steps, 2 advisory finding(s))`, the two advisories being that the
campaign declares no death loop and no mandatory combat to prove. The first
PackTest run of this build found an engine defect, fixed on the spec's branch
before this was written: the runner's server read the heap statement from a
path only the shipped image has and booted at the pin while the runner
asserted the build's number.

`delvec grammar audit --campaign-root .` over the whole content tree reds on
two campaigns that predate this one (`doune-castle-tour` and `vesperhold` hold
zone programs and no `zones.json`); this campaign's manifest names both of its
zones at the region and seed they are built at.

## Build and play

```sh
delvec build campaigns/the-lamp-across-the-water -o .out/lamp --prefabs prefabs
tools/creator/playtest-server.sh up campaigns/the-lamp-across-the-water --prefabs prefabs --out "$PWD/.out/lamp"
```

Start the server, then in the Minecraft Java client at the version the engine
names: Multiplayer → Direct Connect → `localhost:25565`. Set your render
distance to at least 20 chunks (Options → Video Settings) — the lamp is not
drawn below it.
