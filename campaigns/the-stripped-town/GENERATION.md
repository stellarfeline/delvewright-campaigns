# The Stripped Town — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0105 pinned: one street of three
houses and a smokehouse; every cupboard in two of the houses is scenery, the
third holds the one parcel the story needs, and the smoker holds a cooked fish
in its result slot; the arrival line says the town was emptied. It is the first
read of whether the line, heard once at arrival, stops a player opening the
containers, and of whether a stocked smoker reads as a find. Small, one
mechanic, minimum cast. The engine caps scenery at two containers per place and
refuses scenery among containers that matter; those rules are the design.

## What was invented here

- The fiction: Saltlow, the herring that moved off, the town going inland in
  the autumn, Ansel Tarrow the ferryman, his sister Marra and her parcel.
- Which houses are which: the net-maker's and the chandler's are the stripped
  pair (two scenery containers each, at the cap); Marra's cottage is the third
  house, holding one chest and nothing else.
- The smoker's three slots: a raw salmon in the input slot, charcoal in the
  fuel slot, a smoked cod in the result slot. A smoker does not fire while its
  result slot holds something its input cannot become, so the world as loaded
  is still; once a player takes the cod, the smoker lights and smokes the
  salmon.
- The arrival line's sound, a barrel lid closing.
- One class, the Carrier, so the kit says why the party is here.

## Engine and language

Built with `delvec 1.13.0, dsl 0.43.0, mc 1.21.11` from the engine's
`feature/containers-are-declared` at
`adc9a8d14740fc736c805880c8505696ff17ceaf` — an unreleased tree, the only one
carrying spec-0105. Its version string is the same number as the released
`delvec--v1.13.0` (which answers `dsl 0.39.0`), so the version alone does not
say which engine built this level; the revision does.

No shipped library taken: every piece is this campaign's own, written as a
grammar program under `programs/` and frozen by `delvec detail` into
`prefabs/the-stripped-town-*`.

Languages: English, and zh-CN transcreated as a sidecar.

## Posture note

The level tells the player one thing outright — the town is empty, and what is
left was left on purpose — and lets the street confirm it. Ansel explains only
the errand, never the town's grief; the end is the boat leaving, not a
reflection on it.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.
