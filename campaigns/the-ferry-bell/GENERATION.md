# The Ferry Bell — generation record

## What the brief pinned, and what was invented

- **Pinned**: the demo-level row for spec-0104 — one shore, a jetty and a
  ferry house; a talk, a sign to read, a lever that opens the ferry house, a
  bell that calls a fight forming up in sight across the water; every title
  in both languages; the `teaching` block in the keeper's voice; no marker
  anywhere; built once with the lever among its rail's fence posts, refused,
  then moved.
- **Invented**: the keeper (Nell Garrow) and her bad arm; the dead on the spit
  and why she will not ring alone; the rain; the notice's wording; the
  net-menders' fence round the spit; the outro.
- **Languages**: English and `zh-cn`. The Chinese was transcreated by the
  engine's translator (`tools/creator/i18n-translate.py`) and two rows were
  written by hand through `delvec l10n-apply`: the quest goal (the translator
  left Nell's name in Latin letters and put her at the jetty's end rather than
  its foot) and the bell's hint, which changed after the translator ran.

## Engine

- An unreleased engine revision, built from source (Init I3b, dev mode):
  `delvec 1.13.0, dsl 0.42.0, mc 1.21.11`, from engine branch
  `feature/guidance-can-be-followed` at
  `4dd07d8cad304d9623daef6870b631732adbd726`. Every document carries
  `dsl_version` 0.42.0. The released `delvec--v1.13.0` answers
  `delvec 1.13.0, dsl 0.39.0`: the same engine number with another dsl, so
  this level does not build with the release, and only the `dsl` number and
  the revision above tell the two apart.
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
  first build, kept as `transcripts/lever-on-the-rail.txt`.
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

Functional text first. Every title opens with its kind's verb; the one hint
gives direction by what the player can already see; Nell's three teaching
lines are in her voice and carry the key as the player's own binding.
