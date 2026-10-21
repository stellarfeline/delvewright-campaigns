# The Bell Changes the Tune — generation record

## What the brief pinned, and what was invented

- **Pinned**: the demo-level row for spec-0109 — a chapel and its yard; the
  yard's atmosphere a soft spaced track (`min_delay` 2400, `max_delay` 6000);
  the chapel's `{}` with `audio/music_volume` 0.0; a dread atmosphere on a
  single-file disc with no gap that replaces; the ground's own silence on
  `horizon`; an `interact` at the bell whose bundle repaints the yard with the
  dread; an environment trigger at the chapel door carrying
  `stop-sound {category: music}`; a final cutscene over the yard declaring
  `hears: atmosphere/dread`; one refusal transcript (an atmosphere with no
  music stated, `DW1031`); English and `zh-cn`.
- **Invented**: Hollin Chapel, the forty years of silence and the vigil book;
  the tracks (`music.overworld.meadow` for the yard, `music_disc.11` for the
  dread — short, so its loop seam comes round inside two minutes); the beat
  out to the yew, which arms the door trigger only after the dread has been
  heard, so the yard's first track is left to fade on the way in; the trigger
  setting `flag/back-under-the-roof`, read by the last objective, so the forced
  route performs it; no cast.
- **Languages**: English and `zh-cn`. The sidecar was transcreated by
  `tools/creator/i18n-translate.py` (DeepSeek; 16 of 16 rows accepted by its
  fact check) and one row, the class blurb, rewritten through
  `delvec l10n-apply`. `README.zh-cn.md` was written in-agent.

## Engine

- An unreleased engine revision, built from source (Init I3b, dev mode):
  `delvec 1.13.0, dsl 0.47.0, mc 1.21.11`, from engine branch
  `feature/music-per-scene` at `8ed5a3abe6da70fd5cdcd9e4740b68e905bead20`.
  Every document carries `dsl_version` 0.47.0. The released `delvec--v1.13.0`
  answers `delvec 1.13.0, dsl 0.39.0` and refuses this level: only the `dsl`
  number and the revision tell the two apart.
- Rebuilt on the assembled Batch-B engine (`integrate/batch-b`, `delvec
  1.13.0, dsl 0.54.0`): every document carries 0.54.0; the ending's id is
  `ending/the-yard-is-still-playing`; the closing shot names its subject, the
  chapel anchor it already looks at. The engine now hands every player a
  compass and a journal.
- Rebuilt on the refreshed engine (`feat/batch-b-refresh` at `351e631e54153b6277fbd02de106f66e92a53583`, `delvec 1.13.0, dsl 0.56.0`):
  every document carries 0.56.0 and `world.json` declares `demo_level: true`;
  nothing a player meets changed. `build` exit 0 twice, byte-identical (194
  files); PackTest 22 of 22 required tests passed; the bot's critical path
  passed; the written world equals the server's at all 2150 compared cells;
  the staging gate admits it with no override (147 rows: 36 bound, 84
  inapplicable, 27 declared uncoverable, 0 refused).
- The skill page used is the one in that engine tree
  (`.claude/skills/delvewright/skills/new-delve/`), which pins
  `delvec--v1.13.0`.
- The prefab library is this repository's own `prefabs/`; the level's two
  pieces are `prefabs/the-bell-changes-the-tune-*`.

## Design gate

Not held. A demo level is confirmed by its owner on the finished thing; no
reference images were drawn, so there is no `design.json` and no
`design/cameras.json`. `world.json` declares `demo_level: true` and the
engine's demo queue names `campaigns/the-bell-changes-the-tune`, so the staging
gate's design-record findings measure this level zero.

## Posture

Functional text first. The objective titles say where to go; the two
narration lines say only what the party can hear, never what the engine does.
The storybook's what-to-listen-for list is the level's real content.

## Machine ladder (round 1)

- `delvec validate` / `delvec build`: exit 0. Build line:
  `music binding: 4 biome(s) a camera can stand in — 3 atmosphere(s) and the
  ground declared (2 with a track, 2 silent: 1 fading, 1 playing out), 0 band
  biome(s) undeclared; 1 cutscene(s), 1 declare what they hear, 1 of 1
  confirmed; 1 stop-sound effect(s), 1 of 1 cut a play-out, 0 a stinger, 0 a
  hiccup; 0 sound(s) in a category other than master`.
- PackTest: 21 of 21 required tests passed, `music_hears_0` among them.
- Written world: exit 0, the server's world equal to the engine's model at
  every compared cell outside the named classes.
- Bot: **red**, on two harness findings, neither a defect of this campaign:
  1. *The dread's listening station* reads `atmosphere/yard` where the ledger
     says `atmosphere/dread`. The repaint reached the client (`4 of 4 held
     chunk(s) told by chunk_biomes`), but the pinned mineflayer 4.37.1 has no
     handler for `chunk_biomes`, so the bot's own world keeps the biome it had
     when the chunk loaded, and any station read after a repaint of an
     already-loaded chunk reads the old biome.
  2. *The door trigger* (`approach`, range 1) is not performed: the harness
     walks to `max(1, range − 1)` of the anchor, which for range 1 leaves no
     margin, and the bot stopped 1.1 blocks from the threshold. A diagnostic
     copy with range 2 (not shipped) performed the trigger, heard the
     `stop_sound` packet and completed the campaign, red only on finding 1.

## Round 2

- **What changed**: the door trigger is an `approach` of range 3 around the
  same `anchor/threshold` mark (range 1 could be walked past, so the ending
  never fired); the ending cutscene declares its own `music`, the lament
  `minecraft:music_disc.mellohi`, with `replace_current_music: true` and no
  delay, beside its `hears: atmosphere/dread`; the storybook in both languages
  states the yard's two-to-five-minute wait between plays, asks for no client
  setting, and listens to the lament's way in and out.
- **Engine**: `delvec 1.13.0, dsl 0.47.0`, built from engine branch
  `feature/music-per-scene` at `4a13c8b5b65bda660605a1c35347fdf05eeb20af`.
- `delvec validate` / `delvec build`: exit 0. Build line:
  `music binding: 6 biome(s) a camera can stand in — 3 atmosphere(s) and the
  ground declared (2 with a track, 2 silent: 1 fading, 1 playing out), 0 band
  biome(s) undeclared; 1 cutscene(s), 1 declare what they hear, 1 of 1
  confirmed, 1 declare their music over 5 painted 4-cell(s) in 4 paint line(s)
  and 2 variant biome(s); 1 stop-sound effect(s), 1 of 1 cut a play-out, 0 a
  stinger, 0 a hiccup; 0 sound(s) in a category other than master`.
- PackTest: 21 of 21 required tests passed, `cutscene_music_0` among them.
- Bot: critical path PASSED, 7 steps, the door trigger performed by approach;
  run report for manifest `0abb88b6d979…`.
- Written world: exit 0, 2150 cells compared, the server's world equal to the
  engine's model at every compared cell outside the named classes.
- Staging gate: REFUSED, 2 of 123 findings unbound — `drill3-01`, `drill3-03`
  (no design record; the design gate was not held for this demo level). Not
  overridden here.
