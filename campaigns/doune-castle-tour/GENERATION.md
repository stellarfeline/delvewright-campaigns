# Doune Castle: A Guided Tour — generation record

## The toolchain this campaign is authored against

- Plugin `delvewright` 1.2.4 (skill `/new-delve`), run in dev mode from the engine
  checkout.
- Engine revision `2bda3edd2f63a7a97b8d46b625f04e67c050fa4d`, `delvec` 1.4.0,
  `dsl_version` 0.24.2, Minecraft 1.21.11.
- Prefab library: the content repository `stellarfeline/delvewright-campaigns`,
  branch `campaign/doune-castle-tour` cut from `cf8b08ba645f6147166ccbf2f951942067bc9271`.
  That is **not** the revision the engine's `[content].sha` names
  (`8e09c30c17c78538ac0b6c36fa5edc5f681a45eb`). No shipped piece is bound; the
  campaign's only piece is its own.

## What the brief pinned, and what was invented

Pinned by the brief:
- a showcase delve with a simple main quest: a guide leads the party through one
  castle;
- the party and the guide start outside, with the whole exterior in view;
- talking to the guide gives the castle's background and history; when the
  conversation ends the guide walks to the next place and waits;
- the party may explore freely or follow the guide;
- the castle is modelled on a real castle, majestic outside, with many rooms,
  each furnished with care, arranged as a working castle rather than unrelated
  rooms in a shell.

Invented here:
- the castle: Doune Castle, chosen for surviving, documented, rectilinear rooms
  and an explicit household circulation chain;
- the nine-stop route and its order, the guide's person and voice;
- the 1.5 blocks-per-metre scale, the `valley` surround, the `day` + `clear` hour;
- the Visitor class and its kit.

Showcase breadth is deliberately **not** pursued: the brief is detailed, so it
gets exactly what it pinned and nothing extra — no combat, bonfires or waves.

## Placement model

`areas[]` with **one area bound to one campaign-built piece** — the whole castle
as a grammar-built site, ringed by a `valley` surround — not a site plan. The
thing the delve is named after has an exterior the player is meant to read, which
the placement test routes to a site plan; but a site plan's walls and roofs are
the derived blockout's fixed legibility palette (`minecraft:stone_bricks` walls,
`minecraft:smooth_stone` flat ceilings), and they stay whole-owned after detail —
a detail piece fills only a place's play space plus its floor course. No
document can give a site-plan exterior battlements, garret roofs or dressed
stone, so a site plan cannot deliver the brief's exterior. A one-piece site is
the shape the engine documents for a building together with its ground, and every
block of it — exterior and interior — is the campaign's own program.

## Posture note

- **Address**: the guide speaks to the visitors directly and about the tour
  itself — the brief's own frame, pushed rather than hidden.
- **Time order**: the history is told in route order, not chronological order —
  1746 arrives in the courtyard before 1425 arrives upstairs.
- **Resolution**: the tour ends unresolved, on the fourth range that was planned
  and never built, not on a summing-up.

## Findings ledger

None yet.
