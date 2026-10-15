# The Ferry Bell — generation record

## What the brief pinned, and what was invented

- **Pinned**: the revised demo-level row for spec-0104 — one shore, a jetty and
  a ferry house; a talk with the keeper that opens two objectives at once; the
  compass each player aims through its menu; `highlight {within: 6}` on the
  lever that opens the ferry house and none on the bell; the fight the bell
  calls forming up in sight across the water; the journal with two manual
  pages in the keeper's voice, `[[key|use]]` on the lever line; built once with
  the lever among its rail's fence posts, refused by `DW0863`, then moved.
- **Departure from the row**: the row's two objectives are the slate and the
  bell. On this engine the bell, behind the bolted door, has to follow the
  lever in the quest's `after` order (`DW0317` otherwise refuses the walk into
  the house; a `use` trigger in the lever's place is refused by the layout
  graph, `DW0816`/`DW0817`, which credits no grant to a trigger). The talk
  opens the slate and the lever; the bell opens once the bolt is drawn.
- **Invented**: the keeper (Nell Garrow; the row's ferryman) and her bad arm;
  the dead on the spit and why she will not ring alone; the rain; the slate's
  wording; the manual's two pages; the net-menders' fence round the spit; the
  outro.
- **Removed by the rewrite**: the `teaching` block; no marker setting was
  declared.
- **Languages**: English and `zh-cn`. The rows this round added or changed
  were written in-agent through `delvec l10n-apply`: the engine's translator
  (`tools/creator/i18n-translate.py`, DeepSeek `deepseek-v4-pro`) held its one
  request open for over twenty minutes without answering and was stopped. The
  rows it had transcreated in the first build are kept.

## Engine

- An unreleased engine revision, built from source (dev mode):
  `delvec 1.13.0, dsl 0.42.0, mc 1.21.11`, from engine branch
  `feature/guidance-can-be-followed` at
  `a4e6639c5652174b8ccd17c63de90ee08fbf71e4`. Every document carries
  `dsl_version` 0.42.0. The released `delvec--v1.13.0` answers
  `delvec 1.13.0, dsl 0.39.0`: the same engine number with another dsl, so
  this level does not build with the release.
- The prefab library is this repository's own `prefabs/`; the level's four
  pieces are `prefabs/the-ferry-bell-*`.

## Design gate

Not held. A demo level is confirmed by its owner on the finished thing; no
reference images were drawn, so there is no `design.json` and no
`design/cameras.json`. The staging gate's two design-record findings
(`drill3-01`, `drill3-03`) stay unbound for that reason.

## How the map is made

- `design/heightmap.py` writes `design/heightmap.png`, the site plan's
  terrain: land at y 63, a one-course beach step flush with the sea wherever
  land meets the water or the region's edge outside the two ground places
  (`DW0322`), the shelf at y 60 and the cove floor at y 56. The water is three
  `volumes[]` of `minecraft:water`, its top at the sea's y 62.
- `design/build_pieces.py` writes the four place programs under `programs/`;
  `delvec detail campaigns/the-ferry-bell --all` freezes them as pieces.
  `--lever-on-rail` writes the jetty with the bolt lever on the rail: the
  first build, kept as `transcripts/lever-on-the-rail.txt`. Regenerating
  without it reproduces the committed pieces byte for byte.
- Decisions the checks forced, each a design change: the bell stands on a
  floor frame (a ceiling-hung bell put the interact shot's camera inside the
  roof, `DW0724`); the east wall's window is a one-course slit at eye level (a
  pane stops the line of sight, and a taller hole is a way out); the beach
  east of the jetty and the spit are fenced where the dead could otherwise
  reach the open sea from their seat (`DW0924`); the dead declare
  `follow_range` 24, so the bell's cell is within their reach across the
  water, and `max_health` 20, so the fight carries a time-to-kill bound; the
  bell sets the party's checkpoint on the jetty, so a death in the fight comes
  back to it.

## Posture

Functional text first. Every title opens with its kind's verb; the slate's and
the bell's hints give the place by what the player can already see; the one
`DW1015` warning (*head* in the slate's hint) is a noun and is kept. The manual
is in Nell's voice and carries the use key as the player's own binding.
