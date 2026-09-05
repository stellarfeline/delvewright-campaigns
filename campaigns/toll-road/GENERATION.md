# The Toll Road — generation record

`dsl_version` 0.19.0 · built against the engine `versions.toml` `[engine].authoring_ref`
pins · `delvec 1.1.0, dsl 0.19.0, mc 1.21.11`.

## The brief

Build the trap demo level: a short fortified pass where every trap type guards one
alcove of loot, and disarm levers teach counterplay. Ten to twenty minutes, minimum
cast, one mechanic in the spotlight. Traps are spec-0011 (the redstone-native
trigger) and spec-0022 (the command payload, with the `volley` and `collapse` trap
verbs).

## Posture note

Three axes pushed off the machine default for this campaign:

- **Morality.** The antagonist is right. The toll was real, the road was cut and
  kept, and the party is taking a service without paying for it. Ottiline is owed.
- **Address.** The keeper addresses the party as customers and quotes the tariff at
  them by clause, which is the nearest thing to breaking the fourth wall that a
  clerk can honestly do.
- **Resolution.** It closes on a ledger entry, not on an internal understanding.
  Nobody is persuaded and nothing is settled; the party is simply recorded.

## Decisions

- **`areas[]`, not a site plan.** Traps bind to prefab anchors — `Trap::at`, a
  `volley`'s `from_anchor`, a `disarm`'s `via`. A site-plan campaign synthesizes
  only `spawn`, `anchor/node-<place>`, `anchor/seam-<edge>` and
  `anchor/unlock-<edge>`, so a site plan has nowhere to hang a trap station.
- **A command payload, not the legacy `dispense` effect.** Under spec-0022 redstone
  keeps only the trigger, so a trap needs no dispenser and no wiring in the piece —
  only a point anchor for the trigger cell. Measured: no piece in the shipped
  library carries a dispenser, pressure plate, tripwire or trapped chest (0 of 36),
  and none declares a trap anchor (0 of 36), so the legacy shape was not authorable
  here at all.
- **The piece is a campaign zone, not a CLI-parameterised library expansion.** The
  first cut was `delve-grammar expand --program boulder-stair --param … --role …`.
  Its metadata records `program`, `program_hash`, `seed` and `region` and claims
  "those four inputs regenerate this NBT byte for byte" — and they do not, because
  neither `--param` nor `--role` is recorded. Measured: regenerating from exactly
  the four recorded inputs gives `3f625175c72b9d2e4a34cd3837a2df21f8e3e9f62394c98d16e387472ad64d44`
  where the artifact is `78e5e210d25b07248183580be72e141407ab5e856e6ef82083d038d2996ae6ae`.
  Baking the parameters and palette into a program file under `design/programs/`
  makes the record true: the hash then names a document that exists in this
  repository. Two expansions from the committed file are byte-identical.
- **The paint was measured, not remembered.** `tools/block-appearance.py --screen`
  over full cubes at `L` 0.35–0.60, `C_mean < 0.035`, `texture_range <= 0.45`, not
  tinted, not gravity — 1146 candidates to 55. Bound `rough` to `minecraft:tuff`,
  `smooth` to `minecraft:stone_bricks`, `lamp` to `minecraft:glowstone`. The mix
  measures `chroma_mass` 0.0144, `chromatic_area` 0.04, loudest member glowstone at
  4% of area; the swatch sheet was read before anything was bound.
- **The pass is lit by design, not by a mitigation.** As expanded from the corpus
  rule it measured `profile: dark`, `measured_min_light` 0 over 413 cells. A sconce
  course in the alcove wall and a second in the vault takes it to `lit`,
  `measured_min_light` 4 over 323 cells, with glowstone at 2.6% of the piece. No
  `mitigation` is declared, because the demo is about seeing a plate and a lever.

## Findings

| # | finding | status |
|---|---|---|
| 1 | **No producer writes an anchor `role`.** `DW0345` requires the spawn area's piece to declare an anchor with `"role": "entry"` (or the legacy names `spawn`/`entry`, which its own message calls a compatibility path for pieces admitted before the role existed). `delve-grammar`'s `mark` cannot declare one — `grammar.md` §7 — and `delve-admit anchor` writes only `pos`, `facing`, `region` and `block`, which `prefab-procedure.md` states outright. So a piece authored today cannot be the piece a party spawns in, and this campaign is blocked at `delvec build` with `DW0345` (exit 3), reproduced on `prefab/toll-road-pass` itself. The obvious escape does not escape: binding a first area to a shipped entry-bearing piece and crossing into the pass on an objective is refused by `DW0872`, which asks the DESTINATION area for the same anchor. Both routes were built and both red. | **engine** |
| 2 | **The same gap closes two more anchor keys.** `dispenser` and `trigger_block` have no producer either. `dispenser` is what a spec-0011 `dispense` trap fills; `trigger_block` is what `DW0363` requires before a trap may carry a flag gate. So a flag-gated trap and a legacy dispense trap are both unauthorable on any piece this toolchain can make. | **engine** |
| 3 | **A grammar expansion's provenance omits `--param` and `--role`** while claiming the recorded inputs reproduce the bytes. Measured above; worked around here by baking both into a committed program file. | **engine** |
| 4 | **The alcoves are one cell deep.** They are the corpus rule's dodge pockets, which is the right shape for a body stepping out of a volley and a poor one for an alcove of loot. A loot alcove wants two or three cells of depth and its own back wall. | open |
| 5 | **`DW0345` is build-tier, so an `areas[]` campaign bound to a piece with no entry anchor validates clean through the skill page's steps 1–7** and only refuses at step 8 — after the design gate has been spent. The page does give the check (step 2A prints the script and the 5-of-36 count); what it has no answer for is what to do when the piece you need does not exist yet. | open |

## Machine record for this round

Validation-loop iterations to green: not reached — the campaign is at the skill
page's step 4 (the design gate), which is the state the page describes as correct
there: a campaign that does not validate, carrying only refusals that
`quests.json` and `dialogue.json` will supply.

DW codes this round hit, with counts:
`DW0150` x1, `DW0152` x1 (both the expected step-3 state);
`DW0345` x1, `DW0872` x1 and `DW0751` x1 (the real refusals);
`DW0727` x2 and `DW0781` x1 (advisories).
