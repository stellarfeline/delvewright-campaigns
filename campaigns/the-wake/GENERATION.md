# The Wake — generation record

## What the brief pinned, and what was invented

Pinned: a funeral-procession demo level off the engine's demo-levels queue,
with actors, staging and cutscenes in the spotlight; mourners walk; a eulogy
sequence; one player choice redirects the procession; ten to twenty minutes;
minimum cast. Everything else — the coast, the sluice, the two roads, the cast
and every line — is invented.

`dsl_version` is `0.19.0`, the number `delvec --version` printed at Init.

## Posture note

Four axes pushed off the machine default for this campaign:

- **Time order.** The decisive fact is withheld until after the choice. The
  party picks a road without knowing whose order opened the sluice, and learns
  it on the shoulder, when the choosing is over and cannot be revisited.
- **Morality.** The antagonist is right. Ceren's case is the better one and the
  campaign never adjudicates it; nothing rewards either road.
- **Resolution.** The ending refuses to explain itself. There is no
  reconciliation beat and no beat of internal understanding — the last thing
  that happens is a spadeful of earth.
- **Emotion rendering.** Characters name feelings in plain words rather than
  clenching anything. Halda's register is "I am angry. Not at you. Lift."

Wave mob names: none. This campaign stages no waves.

## Placement model, and why

A **site plan**, not `areas[]`. The page's own rule decides it: the party
carries a bier somewhere and the walking is the content, and there is no piece
in the library that is the burial road this delve is about.

It also removes a constraint rather than designing around one. A multi-area
`areas[]` procession needs an entry anchor in every area a beat crosses into,
and **5 of the 36 shipped prefabs declare one** — `cave-shore`, `hello-room`,
`island-beach-camp`, `island-galley`, `keep-spawn-hall` — measured here with
the probe the skill page prints, which reproduced the page's own count and
names exactly. Those five are from four unrelated families, so a coherent
multi-area coast procession is not assemblable from this library. A site-plan
campaign binds no piece at all, so the constraint does not arise.

The four pools were read before this was settled: `pool/stone-keep` (12),
`pool/vertical-keep` (13), `pool/cave-shore` (13), `pool/island` (4).
`pool/island` is the only open-air one and could have carried an outdoor
carry, but its two connectors — `island-greenfield` and
`island-greenfield-bend` — declare the same anchor names, so a jigsaw that
seats either twice makes every station on the route ambiguous. A procession
needs an unambiguous stand at each station, which the synthesized
`anchor/node-<place>` set and declared `stations[]` give without a seating
lottery.

## Design decisions the graph forced

**Both roads end at the same grave.** The first draft buried him in a different
place per branch. That put a mandatory beat in `node/drowned-field`, which the
critical path never visits, and `DW0817` refused it in exactly those words.
The repair was not a graph patch: the fork became a choice about what the
procession is walked through rather than about which ground receives him, which
is a better argument for Ceren and puts one mandatory laying-down beat on the
path.

**The map was rescaled once.** At 48 and 24 the route measured 150 blocks and
`DW0822` projected 3 minutes. The coast road went to 96 and each branch road to
40; the route now measures 214 blocks, about 4 minutes, against a
`target_minutes` of 12. The gap is deliberate and is not walking: the eulogy
sequence, the road argument, the choice and the burial are the other eight
minutes. Whether the carry actually reads as a procession is a question for the
walk, and it is on the list handed over with it.

## Round 1 machine record

Stage 3 ended at the state the page describes: **14 refusals**, every one of
them naming something only `quests.json` or `dialogue.json` can supply.

`DW0818` x6, `DW0152` x3, `DW0172` x2, `DW0482` x2, `DW0150` x1.

Advisories: `DW0822` x1 (the pacing line above), `DW0813` x1 (11 of 11 building
metrics provisional — the metrics gym has not been walked; true of any campaign
on this engine).

Codes hit and cleared during authoring: `DW0100` x1 (an `ally` NPC role the
schema does not define — the enum is `quest-giver` or `flavor`), `DW0828` x2
(two seams allocated on faces the boxes did not share on y), `DW0817` x1 (the
per-branch grave, above). Validation-loop iterations to the stage-3 state: 4.

`delvec fmt`: examined 9 file(s); reformatted 9, 0 unparseable.

## Findings ledger

| # | finding, as observed | round | status |
|---|---|---|---|
| 1 | A `campaign/*` branch cannot be pushed to after the branch is created: `protect-campaign-branches` requires the `NBT palette audit` context on every non-creating push, and `prefab-audit.yml` triggers only on `pull_request` and `workflow_dispatch`, so no push-triggered run can ever report it. | 1 | open |
| 2 | The skill page tells the author to check the series anchor in "the `chain_from` field in the sidecars". `refimg.py` writes it at `request.chain_from`; the top level has no such key, so a reader who checks as the page words it reads `None` on a correctly-anchored image. | 1 | open |
| 3 | The page states that a chained call joins the interaction it was chained from, "so every sidecar in the series carries the same `.id`". Measured on this series against `gemini-native` / `gemini-3.1-flash-image`: every chained sidecar carries a **different** `.id` from view 1's. The anchor still took — `request.chain_from` names view 1 in each — but the page's stated check does not hold on this provider. | 1 | open |
| 4 | Step 2B says the whole map gets a reference of its own *before* the three plan documents are written. This run wrote the plan first and drew the reference after, so the composition was not written against a criterion. The views were then read back against the brief's facts and agree on route order and on both roads rejoining; the plan view puts the shoulder at the junction rather than as its own place, which is the sequence-generation trade the page names. | 1 | ruled |

## Where this campaign stands

Stopped at **step 4, the design gate**, which is the user's. Nothing of step 5
is written. `quests.json` and `dialogue.json` are envelope stubs.
