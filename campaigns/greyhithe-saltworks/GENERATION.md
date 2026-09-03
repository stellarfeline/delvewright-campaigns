# Generation record — the Saltworks at Greyhithe

**This campaign is a rehearsal of the `/new-delve` page at twenty-plus places.
It is not staged, not released, and not a campaign of record.** It exists to
find out where the page, the engine and the prefab method stop an author at
that scale. Nothing in it is approved by anyone.

- date: 2026-09-03
- `dsl_version`: 0.19.0 on every document
- engine: `delvec 1.1.0, dsl 0.19.0, mc 1.21.11`, built from
  `stellarfeline/delvewright` at `0c5f45ee4a9d29ac332175a49d517d52f1210fbe`
- page: `.claude/skills/new-delve/SKILL.md` v1.9.0 at
  `fda97fc08aef0c869b0ee9d366df6d131f31a26c`

## The prompt, verbatim

> A delve for 1–4 players, about 150 minutes, one connected map with at least
> twenty distinct places the party walks through, each with its own purpose in
> the story. Setting: the Saltworks at Greyhithe — a cliffside salt-boiling works
> and the small abbey that owned it, abandoned after the sea took the lower pans;
> the light on the headland still burns and nobody knows who tends it. The whole
> place must read as one hand built it: one masonry, one way of letting light
> in, one silhouette from the sea. Souls-adjacent pacing: a bonfire, one
> shortcut that loops back, one point of no return, one boss. Three classes.
> English only.

## Placement model, and why

**A site plan.** The page's rule: take a site plan "whenever the map is the
point: when the brief describes a place with a shape, when the party has to
walk somewhere and the walking is the content, when there is no prefab that is
the building the story is about." All three hold. There is no boiling house in
the prefab library and there was never going to be one; the brief pins twenty
places *the party walks through*, which is `areas[]`'s exact failure case —
areas sit 256 blocks apart across void with no walkable link, so a
twenty-area campaign would be twenty teleports.

## Decisions

- **Twenty-four places, not twenty.** Twenty is the floor the prompt sets. The
  count came out of the site: three terraces and a headland, and every place
  earns its beat. Twenty-four is also above the largest thing the engine has
  ever been asked to build (the metrics gym, at eighteen).
- **`horizon: "ocean"`** with a default `boundary`, because the brief is a
  headland. The engine refuses `ocean` without a boundary (`DW0320`).
- **`time: "dusk"`, `weather: "clear"`.** The one beat the prompt insists on is
  a lamp that is still burning, and a burning lamp does not read at noon.
  Recorded as a risk for the walk: the open half of this map is most of it.
- **`difficulty: "hard"`.** The page: absent, a wave campaign derives `easy`,
  which halves incoming damage. A souls-adjacent brief wants the real number.
- **One branch point, at the prior's lodging.** The prompt does not ask for a
  fork. This one is not a mechanic bolted on: the prompt's own hook — *nobody
  knows who tends it* — has exactly one interesting answer, which is that
  somebody does and had a reason, and the only decision the party can make
  about that is what leaves the room with them. Two endings, neither right.
- **One vision edge and three views.** `view/from-the-sea` is the brief's third
  rule made into a thing the walk can stand at; the vision edge is the lamp
  seen once from the beach.

## Posture note (writing craft §B)

Three axes pushed off the machine default, for this campaign:

1. **Time order.** The delve is told backwards. The party arrives after every
   event in the story has finished and walks from the newest ruin to the oldest
   cause; the last thing they learn is the first thing that happened.
2. **Morality.** The antagonist is right. Warden Aumery drowned the lower pans
   deliberately and the headland is still standing because of it; the community
   starved for the same reason. Neither ending resolves that.
3. **Thematic explicitness, inverted.** Nobody states the story's point, the
   ending refuses to explain itself, and one thread — why the prior stayed —
   is never answered by anybody.

Plus one deliberate counter to the somatic default: **Sister Elent names her
fear in plain words** rather than clenching anything.

Wave-name note for localization: this campaign reuses no mob name across
waves; every stack that shares a fiction shares a byte-identical string.

## Findings ledger

Kept in `$R/findings.md` for this round rather than here, because the findings
are about the *page and the engine*, not about this campaign. Nothing in this
campaign has been playtested and no finding here has a round number.

## Round record

| round | what it was | rounds to green | codes hit |
|---|---|---|---|
| 1 | generation, steps 1–4 | — | see the round summary |
