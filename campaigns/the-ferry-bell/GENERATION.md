# The Ferry Bell — generation record

## What the brief pinned, and what was invented

- **Pinned**: the revised demo-level row for spec-0104 — one shore, a jetty and
  a ferry house; a talk with the keeper that opens two objectives at once; the
  compass each player aims through its menu; `highlight {within: 6}` on the
  lever that opens the ferry house and none on the bell; the fight the bell
  calls forming up in sight across the water; the journal with two manual
  pages in the keeper's voice, `[[key|use]]` on the lever line; built once with
  the lever among its rail's fence posts, refused by `DW0863`, then moved.
- **The row's shape, kept**: the talk opens the slate and the bell together;
  the bell stands inside the bolted ferry house; the lever beside the door is
  a `use` trigger carrying the highlight, and its `set-flag` is what the
  layout graph's barred edge reads. Gated on `flag/heard-nell`, which the talk
  sets, so the walk does not pull it before the talk.
- **The slate's words** are narration printed on the click: the engine has no
  surface for a placed sign's text, so the sign itself is blank.
- **Invented**: the keeper (Nell Garrow; the row's ferryman), her bad arm and
  her place at the jetty foot;
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
  `sync/main-into-guidance` at
  `f6c553a9ee0554f934d2cc398d8e29f9f26da63a` (`main` merged into
  `feature/guidance-can-be-followed`; binary sha256
  `f8520f03a0c3040b113e96b15710e77cbb25c3e5d7b502ca982db17f0e08ebad`). Every document carries
  `dsl_version` 0.42.0. The released `delvec--v1.13.0` answers
  `delvec 1.13.0, dsl 0.39.0`: the same engine number with another dsl, so
  this level does not build with the release.
- Rebuilt on the assembled Batch-B engine (`integrate/batch-b`, `delvec
  1.13.0, dsl 0.54.0`): every document carries 0.54.0; the ferry door is a
  `walk` with its `gating` (the `barred` class is retired); the ending's id is
  `ending/the-ferry-is-coming`; the ground states the ocean's own vanilla
  music; the two empty barrels are declared scenery with one arrival line.
- Rebuilt on the refreshed engine (`feat/batch-b-refresh` at `351e631e54153b6277fbd02de106f66e92a53583`, `delvec 1.13.0, dsl 0.56.0`):
  every document carries 0.56.0 and `world.json` declares `demo_level: true`;
  nothing a player meets changed. `build` exit 0 twice, byte-identical (221
  files); PackTest 42 of 42 required tests passed; the bot's critical path and
  die-retry stages passed; the written world equals the server's at all 17895
  compared cells; the staging gate admits it with no override (147 rows: 57
  bound, 63 inapplicable, 27 declared uncoverable, 0 refused).
- The prefab library is this repository's own `prefabs/`; the level's four
  pieces are `prefabs/the-ferry-bell-*`.

## Design gate

Not held. A demo level is confirmed by its owner on the finished thing; no
reference images were drawn, so there is no `design.json` and no
`design/cameras.json`. `world.json` declares `demo_level: true` and the
engine's demo queue names `campaigns/the-ferry-bell`, so the staging gate's
design-record findings (`drill3-01`, `drill3-03`) measure this level zero and
admit it.

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
  roof, `DW0724`); Nell stands at the jetty foot in line with the deck's
  west plank, because from one block west and one north the rail's shore-end
  lantern hid the lever (`DW0863`); the east wall's window is a one-course slit at eye level (a
  pane stops the line of sight, and a taller hole is a way out); the beach
  east of the jetty and the spit are fenced where the dead could otherwise
  reach the open sea from their seat (`DW0924`); the dead declare
  `follow_range` 24, so the bell's cell is within their reach across the
  water, and `max_health` 20, so the fight carries a time-to-kill bound; the
  bell sets the party's checkpoint on the jetty, so a death in the fight comes
  back to it.

## Posture

Functional text first. Every title opens with its kind's verb; the slate's and
the bell's hints give the place by what the player can already see. The manual
is in Nell's voice and carries the use key as the player's own binding.
