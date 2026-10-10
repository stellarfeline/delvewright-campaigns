# The Heart Under the Floor — generation record

- **Brief**: the engine's `docs/demo-levels.md` row for pulses (spec-0102). It
  pins a house of three rooms, a heartbeat from under the hearth heard in every
  room and loudest at the hearth, the three flags and their beats, and the two
  pulses' numbers. Everything else here is invented.
- **Engine**: `delvec 1.12.0, dsl 0.39.0`, built from the unreleased engine
  branch that carries spec-0100 to spec-0102. `dsl_version` is `0.39.0` on every
  document.
- **Placement**: a site plan. The library has no house piece, and the cottage
  is the thing the delve is named after. The three rooms are one place,
  `node/cottage`, so the pulses name it with `place`; the rooms are divided by
  walls inside its piece. Three places side by side under one gabled roof was
  tried first and refused (`DW0827`): each roofed place's eaves reach into its
  neighbour's roof zone.
- **The door**: the row's beat is the party shutting the door behind them. The
  front doorway is an open portal (an opening every cell of which must stay
  clear), and a door that shuts behind the party would be a barred way the
  party is shut inside. That device is not in this level; the beat is the party
  stepping past the front door into the front room, and the flag keeps the
  row's name, `flag/door-shut`.
- **The hearthstone**: the piece lays a stone slab on the floor in front of the
  fire, over a block of sculk catalyst set into the floor course. Lifting the
  stone is a `set-block` of air on `anchor/hearth`; what is under it is then in
  plain sight, and the pulses sound from that block's cell.
- **The exit beat**: a fourth objective, on the doorstep, so the party has
  somewhere to stand and listen to the silence after the beat stops, and so the
  bot has a cell outside the cottage to stand on.
- **Languages**: English only.
- **Posture note**: (1) the second person throughout — the narration talks to
  the player; (2) the player's fear is named outright once, at the quickening,
  not rendered in the body; (3) the ending does not explain itself — nothing
  says what the thing under the floor was.
- **The design gate**: not held. No reference art was drawn and no design
  record is approved: `design.json` does not exist, and the staging gate
  counts that as a zero. The design of record is the demo-levels row and
  `DESIGN.md`; the level is handed over built, for its first walk.
