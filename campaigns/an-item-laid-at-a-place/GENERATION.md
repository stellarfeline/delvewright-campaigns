# An Item Laid at a Place — generation record

## What the brief pinned down

The engine's `docs/demo-levels.md` row for spec-0114 pinned: a small chapel
loft at dusk; the party takes a muster roll from a chest below, climbs to the
loft, and lays the roll on the lectern there; the objective is titled with a
placing word (*Lay the roll on the lectern*); the roll leaves the hand at the
click; the lectern then shows it, through a `set-block` of a lectern holding a
book in `on_objective_complete`; a second beat hangs a lantern on a hook the
same way. Its "what to look for": the roll is gone from the inventory the
moment the lectern is used, the lectern shows it, and nothing completes on
arrival alone.

## What was invented here

- The fiction: the chapel of Wending Cross, the muster at first light, the
  clerk who keeps the roll, the night watch the lantern is for.
- The lantern's source: a barrel at the foot of the loft stair, adopted by a
  second `collect`, so that each loft beat has its own item taken from the
  nave below.
- The hook: the bottom link of an iron chain hanging from the loft ceiling.
  The `interact` prop is that link; hanging the lantern replaces it with a
  lantern that hangs from the chain above.
- No objective for climbing to the loft, and no `after` on the two loft beats:
  arriving there is not a beat, the lectern and the hook stand from the start,
  and the first thing the loft completes on is a click with an item held.
- The loft's front is a glazed screen beside the stair's doorway. An open rail
  there was tried first and refused (`DW0836`, an opening in the shared wall
  the plan never allocated).
- The loft is five high inside, not four: the build's fixed interact camera
  over the hook (anchor + 2.5, + 3, + 2.5) stood in the loft's lid at four
  (`DW0724`), and in its east wall until the hook moved west of the lectern.

## Engine and language

- `delvec 1.13.0, dsl 0.51.0, mc 1.21.11`, built from source from the engine's
  `feature/an-objective-says-its-act` at
  `342b8a64dcb1b3b0989570b2d782c6c5f6d27029`, the unreleased tree that carries
  spec-0114. Its version string is the same as the released `delvec--v1.13.0`,
  so the revision, not the version, says which engine built this level.
- No shipped library taken: every piece is this campaign's own.
- Languages: English, and `zh-cn` transcreated from the English.

## The design gate

Not held. A demo level is confirmed on the finished thing: no reference images
were drawn, so there is no `design.json` and no `design/cameras.json`.

## Placement

A site plan of two roofed places on open, flat grass: the nave, pinned, and
the loft hung off its south face by the stair seam, five up. The chapel is
sealed: there is no door to the churchyard, so no ground outside is reached.
Both places are detailed from `programs/<place>.json`, written by
`design/build_pieces.py`; re-run it, then `delvec fmt` and `delvec detail .
--all`, after any plan edit.

## What the lectern can hold

Read from the pinned jar (`minecraft_server.1.21.11.jar`, sha256
`f83b8e093865806f931c7e34aae41b177d4c076335263dd124c75d6d65dd1726`, and the
client jar, sha256
`1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd`):

- Block state: `facing` (north, south, west, east), `has_book`, `powered`
  (the data generator's `reports/blocks.json`).
- Block entity: `Book` (an item stack) and `Page` (an int), the two keys
  `LecternBlockEntity` loads and saves.
- What is drawn: the client's lectern renderer draws the book from `has_book`
  alone; the block model is the same with and without it.
- In adventure mode the book cannot be taken: the lectern menu's *take book*
  button is refused unless `Player.mayBuild()`, on the server and on the
  client screen.

`set-block` writes a block id with a block-state suffix and no block-entity
data, so `minecraft:lectern[facing=south,has_book=true]` is what it can
express: the lectern shows a book and holds none. Opened, the book is empty.
The level says so in the storybook and claims nothing more.

## Posture note

Three axes off the default: the level addresses the player in the second
person only in its hints and its one empty-handed line, never in narration;
the stakes are never stated (nobody says why the names must be read, or what
the muster is for); and it ends on a plain fact, the roll under the lantern,
with no feeling reached.
